"""Number platform for Hinen writable setpoints (SOC limits, charge/discharge power)."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HinenDataUpdateCoordinator
from .entity import HinenControlEntity


@dataclass(frozen=True, kw_only=True)
class HinenNumberEntityDescription(NumberEntityDescription):
    """Describes a Hinen writable number, including its input mode."""

    mode: NumberMode = NumberMode.AUTO


# Ranges/steps come from the device's own property ``specs``.
NUMBER_DESCRIPTIONS: tuple[HinenNumberEntityDescription, ...] = (
    HinenNumberEntityDescription(
        key="BatChgMaxSoc",
        name="Max Charge SOC",
        native_min_value=10,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.BATTERY,
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
    ),
    HinenNumberEntityDescription(
        key="ChargeStopSOC",
        name="Forced Charge Cutoff SOC",
        native_min_value=10,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.BATTERY,
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
    ),
    HinenNumberEntityDescription(
        key="LoadFirstStopSOC",
        name="Min Discharge SOC",
        native_min_value=10,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.BATTERY,
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
    ),
    HinenNumberEntityDescription(
        key="GridFirstStopSOC",
        name="Forced Discharge Cutoff SOC",
        native_min_value=10,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.BATTERY,
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
    ),
    HinenNumberEntityDescription(
        key="ChargePowerSet",
        name="Charge Power Limit",
        native_min_value=0,
        native_max_value=655340,
        native_step=10,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        mode=NumberMode.BOX,
        entity_category=EntityCategory.CONFIG,
    ),
    HinenNumberEntityDescription(
        key="DischargePowerSet",
        name="Discharge Power Limit",
        native_min_value=0,
        native_max_value=655340,
        native_step=10,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        mode=NumberMode.BOX,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hinen number controls."""
    coordinator: HinenDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        HinenNumber(coordinator, device_id, description)
        for device_id in coordinator.devices
        for description in NUMBER_DESCRIPTIONS
    )


class HinenNumber(HinenControlEntity, NumberEntity):
    """A writable Hinen setpoint with verified writes."""

    entity_description: HinenNumberEntityDescription

    def __init__(self, coordinator, device_id, description) -> None:
        """Initialize the number and apply its input mode."""
        super().__init__(coordinator, device_id, description)
        self._attr_mode = description.mode

    @property
    def native_value(self) -> float | None:
        """Return the current setpoint."""
        value = self._raw_value()
        return float(value) if value is not None else None

    async def async_set_native_value(self, value: float) -> None:
        """Write the setpoint (integer) and verify the device applied it."""
        await self._async_write(int(value))
