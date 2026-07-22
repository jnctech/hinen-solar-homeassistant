"""Tests for the control platforms (number/select) and verified writes."""

from __future__ import annotations

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .conftest import (
    DEVICE_INFO_RESPONSE,
    DEVICE_INFO_URL,
    DEVICES_RESPONSE,
    DEVICES_URL,
    PROPERTY_SET_URL,
)

NUMBER_EID = "number.single_phase_hybrid_inverter_forced_charge_cutoff_soc"
SELECT_EID = "select.single_phase_hybrid_inverter_work_mode"


async def _setup(hass: HomeAssistant, aioclient_mock, entry: MockConfigEntry) -> None:
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, json=DEVICE_INFO_RESPONSE)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_number_entity_created(hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry) -> None:
    """The SOC number is created with the device's current value + range."""
    await _setup(hass, aioclient_mock, mock_config_entry)
    state = hass.states.get(NUMBER_EID)
    assert state is not None
    assert state.state == "70.0"
    assert state.attributes["min"] == 10
    assert state.attributes["max"] == 100


async def test_verified_write_success(hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry) -> None:
    """A write the device reflects back succeeds and issues the PUT."""
    await _setup(hass, aioclient_mock, mock_config_entry)
    aioclient_mock.put(PROPERTY_SET_URL, json={"code": "00000", "data": None})
    await hass.services.async_call(
        "number",
        "set_value",
        {"entity_id": NUMBER_EID, "value": 70},
        blocking=True,
    )
    assert any(call[0].upper() == "PUT" for call in aioclient_mock.mock_calls)


async def test_verified_write_detects_unapplied(
    hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry
) -> None:
    """If the device doesn't report the new value/shadow, the write raises."""
    await _setup(hass, aioclient_mock, mock_config_entry)
    aioclient_mock.put(PROPERTY_SET_URL, json={"code": "00000", "data": None})
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            "number",
            "set_value",
            {"entity_id": NUMBER_EID, "value": 80},  # device still reports 70
            blocking=True,
        )


async def test_verified_write_api_rejection(
    hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry
) -> None:
    """A non-'00000' PUT body raises instead of silently succeeding."""
    await _setup(hass, aioclient_mock, mock_config_entry)
    aioclient_mock.put(PROPERTY_SET_URL, json={"code": "A0400", "msg": "denied", "data": None})
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            "number",
            "set_value",
            {"entity_id": NUMBER_EID, "value": 70},
            blocking=True,
        )


async def test_work_mode_select_created(
    hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry
) -> None:
    """The work-mode select maps the enum value to its label + lists options."""
    await _setup(hass, aioclient_mock, mock_config_entry)
    state = hass.states.get(SELECT_EID)
    assert state is not None
    assert state.state == "Self-use"
    assert "Battery priority" in state.attributes["options"]
