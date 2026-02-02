"""DataUpdateCoordinator for Hinen Solar."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import HinenApiClient
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class HinenDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Hinen Solar data."""

    def __init__(self, hass: HomeAssistant, api: HinenApiClient) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api
        self.devices: dict[str, dict[str, Any]] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            # Get list of devices
            devices = await self.api.async_get_devices()

            device_data = {}
            for device in devices:
                device_id = str(device["id"])

                try:
                    # Get detailed device information with properties
                    device_info = await self.api.async_get_device_info(device_id)

                    # Store device data with properties
                    device_data[device_id] = {
                        "id": device_id,
                        "name": device_info.get("deviceName", f"Device {device_id}"),
                        "serial_number": device_info.get("serialNumber"),
                        "model_code": device_info.get("modelCode"),
                        "product_name": device_info.get("productName"),
                        "firmware_version": device_info.get("firmwareVersion"),
                        "status": device_info.get("status"),
                        "alert_status": device_info.get("alertStatus"),
                        "properties": self._parse_properties(
                            device_info.get("properties", [])
                        ),
                    }

                except Exception as err:
                    _LOGGER.error(
                        "Error fetching data for device %s: %s", device_id, err
                    )
                    continue

            self.devices = device_data
            return device_data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def _parse_properties(
        self, properties: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Parse properties array into a dictionary."""
        parsed = {}
        for prop in properties:
            identifier = prop.get("identifier")
            if identifier:
                parsed[identifier] = {
                    "name": prop.get("name"),
                    "value": prop.get("value"),
                    "shadow": prop.get("shadow"),
                    "timestamp": prop.get("timestamp"),
                    "datatype": prop.get("datatype"),
                    "specs": prop.get("specs"),
                }
        return parsed

    def get_device_property(
        self, device_id: str, property_id: str
    ) -> Any | None:
        """Get a specific property value for a device."""
        device = self.devices.get(device_id)
        if not device:
            return None

        properties = device.get("properties", {})
        prop = properties.get(property_id)
        if not prop:
            return None

        return prop.get("value")

    def get_device_name(self, device_id: str) -> str:
        """Get the name of a device."""
        device = self.devices.get(device_id)
        if device:
            return device.get("name", f"Device {device_id}")
        return f"Device {device_id}"
