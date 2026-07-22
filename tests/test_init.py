"""Setup/teardown tests — exercises __init__, coordinator and sensor together."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .conftest import (
    DEVICE_INFO_RESPONSE,
    DEVICE_INFO_URL,
    DEVICES_RESPONSE,
    DEVICES_URL,
)


async def _setup(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_setup_creates_entities(hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry) -> None:
    """A valid entry loads and produces live sensor states from parsed properties."""
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, json=DEVICE_INFO_RESPONSE)

    await _setup(hass, mock_config_entry)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    soc = hass.states.get("sensor.single_phase_hybrid_inverter_battery_state_of_charge")
    assert soc is not None
    assert soc.state == "28"

    # The yield sensor discovered during live validation.
    yield_state = hass.states.get("sensor.single_phase_hybrid_inverter_total_yield")
    assert yield_state is not None
    assert yield_state.state == "13591.3"

    # Battery-charging binary sensor: BatteryPower (1074 W) > 0 → charging.
    charging = hass.states.get("binary_sensor.single_phase_hybrid_inverter_battery_charging")
    assert charging is not None
    assert charging.state == "on"


async def test_unload_entry(hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry) -> None:
    """The entry unloads cleanly."""
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, json=DEVICE_INFO_RESPONSE)

    await _setup(hass, mock_config_entry)
    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_missing_property_is_unknown(
    hass: HomeAssistant, aioclient_mock, mock_config_entry: MockConfigEntry
) -> None:
    """A sensor whose identifier isn't in the payload reports unknown, not an error."""
    aioclient_mock.get(DEVICES_URL, json=DEVICES_RESPONSE)
    aioclient_mock.get(DEVICE_INFO_URL, json=DEVICE_INFO_RESPONSE)

    await _setup(hass, mock_config_entry)
    # Pv1Voltage is a defined sensor but not in the trimmed test payload.
    state = hass.states.get("sensor.single_phase_hybrid_inverter_pv1_voltage")
    assert state is not None
    assert state.state == "unknown"
