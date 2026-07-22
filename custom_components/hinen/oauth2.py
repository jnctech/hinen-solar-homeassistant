"""OAuth2 implementation for Hinen Solar, tied to HA Application Credentials.

Hinen's OAuth is non-standard: the token endpoint is a GET with query params, and
the token response carries the regional data-center ``host`` plus the ``regionCode``.
We therefore override the authorize-URL builder and the token exchange/refresh on
HA's ``AuthImplementation``. The token requests are our own code — no third-party
Hinen client library is used.
"""

from __future__ import annotations

import logging
import secrets
from typing import Any, cast

import jwt
from aiohttp import ClientResponse, web
from homeassistant.components.application_credentials import AuthImplementation
from homeassistant.components.http import KEY_HASS, HomeAssistantView
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from yarl import URL

from .const import (
    CALLBACK_PATH,
    GRANT_TYPE_AUTHORIZATION_CODE,
    GRANT_TYPE_REFRESH_TOKEN,
    TOKEN_CLIENT_ID,
    TOKEN_CLIENT_SECRET,
    TOKEN_HOST,
    TOKEN_REGION_CODE,
)

_LOGGER = logging.getLogger(__name__)

# Query-param key Hinen appends to the callback with the account's region.
_REGION_QUERY_KEY = "regionCode"


class HinenConfigEntryAuth:
    """Supplies a valid access token + data-center host, refreshing as needed."""

    def __init__(self, oauth_session: config_entry_oauth2_flow.OAuth2Session) -> None:
        """Initialize with the entry's OAuth2 session."""
        self._oauth_session = oauth_session

    async def check_and_refresh_token(self) -> str:
        """Ensure the token is valid and return the access token."""
        await self._oauth_session.async_ensure_token_valid()
        return self._oauth_session.token["access_token"]

    async def async_get_token_and_host(self) -> tuple[str, str]:
        """Return a fresh (access_token, host) pair for API requests."""
        await self._oauth_session.async_ensure_token_valid()
        token = self._oauth_session.token
        return token["access_token"], token[TOKEN_HOST]


class HinenOAuth2Implementation(AuthImplementation):
    """Hinen-specific OAuth2 implementation."""

    # Set by the config flow before generating the authorize URL. Unused at
    # runtime, where the reconstructed implementation only refreshes tokens.
    auth_language: str | None = None
    redirect_base: str | None = None

    @property
    def redirect_uri(self) -> str:
        """Return the local callback URL Hinen redirects back to."""
        base = (self.redirect_base or "").rstrip("/")
        return f"{base}{CALLBACK_PATH}"

    async def async_generate_authorize_url(self, flow_id: str) -> str:
        """Build the Hinen authorization URL for the user to open."""
        secret = self.hass.data.get(config_entry_oauth2_flow.DATA_JWT_SECRET)
        if secret is None:
            secret = self.hass.data[config_entry_oauth2_flow.DATA_JWT_SECRET] = secrets.token_hex()
        state = jwt.encode(
            {"flow_id": flow_id, "redirect_uri": self.redirect_uri},
            secret,
            algorithm="HS256",
        )
        # authorize_url ends with a '#/auth' SPA fragment; the query lives after
        # it and the redirect URL is passed unencoded, matching the working flow.
        return (
            f"{self.authorize_url}?state={state}"
            f"&language={self.auth_language or 'en_US'}"
            f"&key={self.client_id}"
            f"&redirectUrl={self.redirect_uri}"
        )

    async def async_resolve_external_data(self, external_data: Any) -> dict:
        """Exchange the authorization code for tokens."""
        return await self._token_request(
            {
                "clientSecret": self.client_secret,
                "grantType": GRANT_TYPE_AUTHORIZATION_CODE,
                "authorizationCode": external_data["code"],
                "regionCode": external_data[TOKEN_REGION_CODE],
            }
        )

    async def _async_refresh_token(self, token: dict) -> dict:
        """Refresh an expired access token, preserving stored extras."""
        new_token = await self._token_request(
            {
                "clientSecret": self.client_secret,
                "grantType": GRANT_TYPE_REFRESH_TOKEN,
                "regionCode": token.get(TOKEN_REGION_CODE),
                "refreshToken": token["refresh_token"],
            }
        )
        return {**token, **new_token}

    async def _token_request(self, params: dict[str, Any]) -> dict[str, Any]:
        """Perform a Hinen token GET request and normalise the response."""
        session = async_get_clientsession(self.hass)
        region_code = params.get("regionCode")
        url = str(URL(self.token_url).with_query(params))

        async with session.get(url) as resp:
            if resp.status >= 400:
                body = await _safe_json(resp)
                _LOGGER.error(
                    "Hinen token request failed (%s): %s",
                    body.get("code", resp.status),
                    body.get("msg", "unknown error"),
                )
            resp.raise_for_status()
            payload = cast(dict[str, Any], await resp.json())

        data = payload.get("data") or {}
        return {
            "access_token": data["accessToken"],
            "refresh_token": data["refreshToken"],
            "expires_in": int(data.get("expiresIn", 3600)),
            TOKEN_HOST: data["host"],
            TOKEN_REGION_CODE: region_code,
            TOKEN_CLIENT_ID: self.client_id,
            TOKEN_CLIENT_SECRET: self.client_secret,
        }


class HinenOAuth2CallbackView(HomeAssistantView):
    """Receives the redirect back from Hinen's OAuth page and resumes the flow."""

    url = CALLBACK_PATH
    name = "auth:hinen_solar:callback"
    requires_auth = False

    async def get(self, request: web.Request) -> web.Response:
        """Handle the OAuth redirect and hand control back to the config flow."""
        if "state" not in request.query:
            return web.Response(text="Missing state parameter", status=400)

        hass = request.app[KEY_HASS]
        state = _decode_jwt(hass, request.query["state"])
        if state is None:
            return web.Response(
                text=("Invalid state. Is Home Assistant configured with the correct external/internal URL?"),
                status=400,
            )

        user_input: dict[str, Any] = {"state": request.query["state"]}
        if "code" in request.query:
            user_input["code"] = request.query["code"]
            user_input[TOKEN_REGION_CODE] = request.query.get(_REGION_QUERY_KEY, "")
        elif "error" in request.query:
            user_input["error"] = request.query["error"]
        else:
            return web.Response(text="Missing code or error parameter", status=400)

        await hass.config_entries.flow.async_configure(flow_id=state["flow_id"], user_input=user_input)
        return web.Response(
            headers={"content-type": "text/html"},
            text="<script>window.close()</script>You may close this window.",
        )


async def _safe_json(resp: ClientResponse) -> dict[str, Any]:
    """Return the JSON body of a response, or an empty dict on failure."""
    try:
        return await resp.json()
    except (ValueError, TypeError):
        return {}


def _decode_jwt(hass: HomeAssistant, encoded: str) -> dict[str, Any] | None:
    """Decode a JWT-encoded state, returning None if invalid."""
    secret = hass.data.get(config_entry_oauth2_flow.DATA_JWT_SECRET)
    if secret is None:
        return None
    try:
        return jwt.decode(encoded, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
