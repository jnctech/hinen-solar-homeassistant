"""Tests for the Hinen REST API client (real client, mocked HTTP)."""

from __future__ import annotations

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.hinen.api import HinenApiClient, HinenApiError

from .conftest import (
    DEVICE_ID,
    DEVICE_INFO_RESPONSE,
    DEVICE_INFO_URL,
    DEVICES_RESPONSE,
    DEVICES_URL,
    HOST,
    error_response,
)


def _client(hass: HomeAssistant) -> HinenApiClient:
    async def _provider() -> tuple[str, str]:
        return "access-token-1", HOST

    return HinenApiClient(async_get_clientsession(hass), _provider)


async def test_get_devices(hass: HomeAssistant, aioclient_mock) -> None:
    """Devices are returned and the token is sent as the Authorization header."""
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    devices = await _client(hass).async_get_devices()
    assert devices[0]["id"] == DEVICE_ID
    # (method, url, data, headers) — the token goes in the Authorization header.
    assert aioclient_mock.mock_calls[0][3]["Authorization"] == "access-token-1"


async def test_get_device_info(hass: HomeAssistant, aioclient_mock) -> None:
    """Device info returns the properties payload."""
    aioclient_mock.get(DEVICE_INFO_URL, json=DEVICE_INFO_RESPONSE)
    info = await _client(hass).async_get_device_info(DEVICE_ID)
    assert info["serialNumber"] == "HTEST0000000000000001"
    assert any(p["identifier"] == "SOC" for p in info["properties"])


async def test_non_success_code_raises(hass: HomeAssistant, aioclient_mock) -> None:
    """A non-'00000' body raises HinenApiError even on HTTP 200."""
    aioclient_mock.get(DEVICES_URL, json=error_response("A0400", "nope"))
    with pytest.raises(HinenApiError):
        await _client(hass).async_get_devices()


async def test_http_error_propagates(hass: HomeAssistant, aioclient_mock) -> None:
    """An HTTP error status is raised (not silently swallowed)."""
    aioclient_mock.get(DEVICES_URL, status=500)
    with pytest.raises(Exception):  # noqa: B017 - aiohttp ClientResponseError
        await _client(hass).async_get_devices()
