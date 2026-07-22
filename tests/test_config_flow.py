"""Tests for the Hinen OAuth2 config flow (real flow, mocked HTTP)."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.setup import async_setup_component

from custom_components.hinen.const import DOMAIN, OAUTH_TOKEN_URL

from .conftest import (
    DEVICE_ID,
    DEVICES_RESPONSE,
    DEVICES_URL,
    TOKEN_RESPONSE,
    error_response,
)

USER_INPUT = {
    "auth_language": "en_US",
    "client_id": "cid",
    "client_secret": "sec",
    "redirect_base": "http://ha.local:8123",
}

CALLBACK_INPUT = {"code": "auth-code", "state": "x", "region_code": "AU"}


async def _advance_to_create(hass: HomeAssistant, flow_id: str):
    """Drive the flow from the external step through creation."""
    # Simulate the OAuth callback resuming the flow with code + region.
    result = await hass.config_entries.flow.async_configure(flow_id, CALLBACK_INPUT)
    if result["type"] == FlowResultType.EXTERNAL_STEP_DONE:
        result = await hass.config_entries.flow.async_configure(flow_id)
    return result


async def test_full_oauth_flow_creates_entry(hass: HomeAssistant, aioclient_mock) -> None:
    """Happy path: user creds → external auth → callback → token → entry."""
    await async_setup_component(hass, "http", {})
    aioclient_mock.get(OAUTH_TOKEN_URL, json=TOKEN_RESPONSE)
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)

    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(result["flow_id"], USER_INPUT)
    assert result["type"] == FlowResultType.EXTERNAL_STEP

    result = await _advance_to_create(hass, result["flow_id"])
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == DEVICE_ID
    assert result["data"]["token"]["access_token"] == "access-token-1"


async def test_flow_aborts_with_no_devices(hass: HomeAssistant, aioclient_mock) -> None:
    """An account with zero devices aborts rather than creating an empty entry."""
    await async_setup_component(hass, "http", {})
    aioclient_mock.get(OAUTH_TOKEN_URL, json=TOKEN_RESPONSE)
    aioclient_mock.get(DEVICES_URL, json={"code": "00000", "msg": "ok", "data": []})

    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], USER_INPUT)
    result = await _advance_to_create(hass, result["flow_id"])
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "no_devices"


async def test_flow_aborts_on_device_fetch_error(hass: HomeAssistant, aioclient_mock) -> None:
    """A device verification failure aborts as cannot_connect."""
    await async_setup_component(hass, "http", {})
    aioclient_mock.get(OAUTH_TOKEN_URL, json=TOKEN_RESPONSE)
    aioclient_mock.get(DEVICES_URL, json=error_response("A0500", "boom"))

    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], USER_INPUT)
    result = await _advance_to_create(hass, result["flow_id"])
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "cannot_connect"
