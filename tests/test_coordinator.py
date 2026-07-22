"""Coordinator tests — per-device availability logging."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.hinen.api import HinenApiClient
from custom_components.hinen.coordinator import HinenDataUpdateCoordinator

from .conftest import (
    DEVICE_INFO_RESPONSE,
    DEVICE_INFO_URL,
    DEVICES_RESPONSE,
    DEVICES_URL,
    HOST,
)


def _coordinator(hass: HomeAssistant) -> HinenDataUpdateCoordinator:
    async def _provider() -> tuple[str, str]:
        return "access-token-1", HOST

    return HinenDataUpdateCoordinator(hass, HinenApiClient(async_get_clientsession(hass), _provider))


async def test_unavailable_device_logs_once(hass: HomeAssistant, aioclient_mock, caplog) -> None:
    """A device that keeps failing is logged once, not on every poll."""
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, status=500)

    coordinator = _coordinator(hass)
    with caplog.at_level(logging.DEBUG):
        await coordinator.async_refresh()
        await coordinator.async_refresh()
        await coordinator.async_refresh()

    # Three polls, one error — subsequent failures drop to debug.
    assert caplog.text.count("Error fetching data for device") == 1
    assert "still unavailable" in caplog.text


async def test_device_recovery_is_logged(hass: HomeAssistant, aioclient_mock, caplog) -> None:
    """When a failing device comes back, the recovery is logged and data returns."""
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, status=500)
    coordinator = _coordinator(hass)
    await coordinator.async_refresh()
    assert not coordinator.devices

    aioclient_mock.clear_requests()
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, json=DEVICE_INFO_RESPONSE)

    with caplog.at_level(logging.INFO):
        await coordinator.async_refresh()

    assert "is available again" in caplog.text
    assert coordinator.devices
