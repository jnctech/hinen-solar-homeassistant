"""Diagnostics tests — the dump must stay useful without leaking secrets."""

from __future__ import annotations

import json

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hinen.diagnostics import async_get_config_entry_diagnostics

from .conftest import (
    DEVICE_ID,
    DEVICE_INFO_RESPONSE,
    DEVICE_INFO_URL,
    DEVICES_RESPONSE,
    DEVICES_URL,
)


async def _setup(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_diagnostics_redacts_credentials_and_identifiers(
    hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry
) -> None:
    """Tokens, client credentials, serial and device id never reach the dump."""
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, json=DEVICE_INFO_RESPONSE)
    await _setup(hass, mock_config_entry)

    diagnostics = await async_get_config_entry_diagnostics(hass, mock_config_entry)
    dumped = json.dumps(diagnostics)

    for secret in (
        "access-token-1",
        "refresh-token-1",
        "client-id-1",
        "client-secret-1",
        "HTEST0000000000000001",
        DEVICE_ID,
    ):
        assert secret not in dumped


async def test_diagnostics_keeps_useful_data(
    hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry
) -> None:
    """Redaction must not gut the dump — operational data still comes through."""
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, json=DEVICE_INFO_RESPONSE)
    await _setup(hass, mock_config_entry)

    diagnostics = await async_get_config_entry_diagnostics(hass, mock_config_entry)

    assert diagnostics["last_update_success"] is True
    device = diagnostics["devices"][0]
    # Model/firmware are product-generic and stay, so support can act on the dump.
    assert device["model_code"] == "SH6KL-SG1-EU"
    assert device["firmware_version"] == "2.1.24"
    assert device["properties"]["SOC"]["value"] == 28
