"""Binary sensor platform for Hinen Solar."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, STATUS_ONLINE
from .coordinator import HinenDataUpdateCoordinator


@dataclass
class HinenBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Hinen binary sensor entity."""

    value_fn: Callable[[dict[str, Any]], bool] | None = None


def is_battery_charging(coordinator: HinenDataUpdateCoordinator, device_id: str) -> bool:
    """Determine if battery is charging based on battery power."""
    battery_power = coordinator.get_device_property(device_id, "BatteryPower")
    if battery_power is None:
        return False
    return float(battery_power) > 0


BINARY_SENSOR_DESCRIPTIONS: tuple[HinenBinarySensorEntityDescription, ...] = (
    HinenBinarySensorEntityDescription(
        key="online",
        name="Online Status",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value_fn=lambda device: device.get("status") == STATUS_ONLINE,
    ),
    HinenBinarySensorEntityDescription(
        key="battery_charging",
        name="Battery Charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hinen Solar binary sensor based on a config entry."""
    coordinator: HinenDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[HinenBinarySensor] = []

    # Create binary sensors for each device
    for device_id in coordinator.devices:
        for description in BINARY_SENSOR_DESCRIPTIONS:
            entities.append(HinenBinarySensor(coordinator, device_id, description))

    async_add_entities(entities)


class HinenBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Hinen Solar binary sensor."""

    entity_description: HinenBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: HinenDataUpdateCoordinator,
        device_id: str,
        description: HinenBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_id = device_id

        device_name = coordinator.get_device_name(device_id)
        self._attr_name = f"{device_name} {description.name}"
        self._attr_unique_id = f"{device_id}_{description.key}"

        # Set device info
        device_data = coordinator.devices.get(device_id, {})
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device_name,
            "manufacturer": "Hinen",
            "model": device_data.get("model_code", "Solar Inverter"),
            "sw_version": device_data.get("firmware_version"),
            "serial_number": device_data.get("serial_number"),
        }

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        if self.entity_description.key == "online":
            # Use the value_fn for online status
            device_data = self.coordinator.devices.get(self._device_id, {})
            if self.entity_description.value_fn:
                return self.entity_description.value_fn(device_data)
            return False

        elif self.entity_description.key == "battery_charging":
            # Check battery power to determine charging state
            return is_battery_charging(self.coordinator, self._device_id)

        return False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not super().available:
            return False

        # Check if the device exists in coordinator data
        return self._device_id in self.coordinator.devices
