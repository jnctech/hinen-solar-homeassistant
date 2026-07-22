"""Tests for the Hinen OAuth2 implementation (token exchange/refresh, authorize URL)."""

from __future__ import annotations

from homeassistant.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant

from custom_components.hinen.const import (
    CALLBACK_PATH,
    DOMAIN,
    OAUTH_AUTHORIZE_URL,
    OAUTH_TOKEN_URL,
)
from custom_components.hinen.oauth2 import HinenOAuth2Implementation, _decode_jwt

from .conftest import HOST, TOKEN_RESPONSE


def _impl(hass: HomeAssistant) -> HinenOAuth2Implementation:
    return HinenOAuth2Implementation(
        hass,
        DOMAIN,
        ClientCredential("cid", "sec"),
        AuthorizationServer(OAUTH_AUTHORIZE_URL, OAUTH_TOKEN_URL),
    )


async def test_resolve_external_data_normalises_token(hass: HomeAssistant, aioclient_mock) -> None:
    """Auth-code exchange maps the camelCase body to the HA token shape + extras."""
    aioclient_mock.get(OAUTH_TOKEN_URL, json=TOKEN_RESPONSE)
    token = await _impl(hass).async_resolve_external_data({"code": "auth-code", "region_code": "AU"})
    assert token["access_token"] == "access-token-1"
    assert token["refresh_token"] == "refresh-token-1"
    assert token["expires_in"] == 3600
    assert token["host"] == HOST
    assert token["region_code"] == "AU"
    assert token["client_id"] == "cid"
    assert token["client_secret"] == "sec"


async def test_refresh_token_preserves_extras(hass: HomeAssistant, aioclient_mock) -> None:
    """Refresh returns fresh tokens while keeping region/client from the old token."""
    aioclient_mock.get(OAUTH_TOKEN_URL, json=TOKEN_RESPONSE)
    old = {
        "access_token": "old",
        "refresh_token": "old-refresh",
        "region_code": "AU",
        "client_id": "cid",
        "client_secret": "sec",
    }
    new = await _impl(hass)._async_refresh_token(old)
    assert new["access_token"] == "access-token-1"
    assert new["region_code"] == "AU"
    assert new["client_id"] == "cid"


async def test_generate_authorize_url(hass: HomeAssistant) -> None:
    """The authorize URL carries key/language/redirect and a JWT state → flow id."""
    impl = _impl(hass)
    impl.auth_language = "en_US"
    impl.redirect_base = "http://ha.local:8123"
    url = await impl.async_generate_authorize_url("flow-123")

    assert url.startswith(f"{OAUTH_AUTHORIZE_URL}?")
    assert "key=cid" in url
    assert "language=en_US" in url
    assert f"redirectUrl=http://ha.local:8123{CALLBACK_PATH}" in url

    state = url.split("state=", 1)[1].split("&", 1)[0]
    decoded = _decode_jwt(hass, state)
    assert decoded is not None
    assert decoded["flow_id"] == "flow-123"


async def test_redirect_uri_strips_trailing_slash(hass: HomeAssistant) -> None:
    """A trailing slash on the base URL does not double up the callback path."""
    impl = _impl(hass)
    impl.redirect_base = "http://ha.local:8123/"
    assert impl.redirect_uri == f"http://ha.local:8123{CALLBACK_PATH}"


def test_decode_jwt_invalid_returns_none(hass: HomeAssistant) -> None:
    """A garbage state decodes to None rather than raising."""
    assert _decode_jwt(hass, "not-a-jwt") is None
