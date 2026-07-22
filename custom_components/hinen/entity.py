"""Base entity for Hinen writable controls (number/select)."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import HinenDataUpdateCoordinator


class HinenControlEntity(CoordinatorEntity[HinenDataUpdateCoordinator]):
    """Shared device info + verified-write helper for Hinen control entities.

    ``entity_description.key`` is the Hinen property identifier that the control
    reads and writes.
    """

    def __init__(
        self,
        coordinator: HinenDataUpdateCoordinator,
        device_id: str,
        description: EntityDescription,
    ) -> None:
        """Initialize the control entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_id = device_id

        device_name = coordinator.get_device_name(device_id)
        self._attr_name = f"{device_name} {description.name}"
        self._attr_unique_id = f"{device_id}_{description.key}"

        device_data = coordinator.devices.get(device_id, {})
        # Same device identifier as the sensors so controls attach to one device.
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{device_id}_advanced")},
            "name": device_name,
            "manufacturer": MANUFACTURER,
            "model": device_data.get("model_code", "Solar Inverter"),
            "sw_version": device_data.get("firmware_version"),
            "serial_number": device_data.get("serial_number"),
        }

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return super().available and self._device_id in self.coordinator.devices

    def _raw_value(self) -> Any:
        """Return the control's commanded (shadow) value, falling back to actual."""
        return self.coordinator.get_device_setpoint(self._device_id, self.entity_description.key)

    async def _async_write(self, value: Any) -> None:
        """Write a value and confirm the device applied it (raises on failure)."""
        await self.coordinator.async_set_property_verified(self._device_id, self.entity_description.key, value)
        self.async_write_ha_state()
