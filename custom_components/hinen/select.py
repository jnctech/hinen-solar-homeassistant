"""Select platform for the Hinen inverter work mode."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, WORK_MODE_OPTIONS
from .coordinator import HinenDataUpdateCoordinator
from .entity import HinenControlEntity

# option label -> device enum value
_LABEL_TO_VALUE = {label: value for value, label in WORK_MODE_OPTIONS.items()}

WORK_MODE_DESCRIPTION = SelectEntityDescription(
    key="WorkModeSetting",
    name="Work Mode",
    entity_category=EntityCategory.CONFIG,
    options=list(WORK_MODE_OPTIONS.values()),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Hinen work-mode select."""
    coordinator: HinenDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        HinenWorkModeSelect(coordinator, device_id, WORK_MODE_DESCRIPTION) for device_id in coordinator.devices
    )


class HinenWorkModeSelect(HinenControlEntity, SelectEntity):
    """Work-mode selector with verified writes."""

    entity_description: SelectEntityDescription

    @property
    def current_option(self) -> str | None:
        """Return the current work mode, or None if it's an unmapped value."""
        return WORK_MODE_OPTIONS.get(self._raw_value())

    async def async_select_option(self, option: str) -> None:
        """Set the work mode and verify the device applied it."""
        if (value := _LABEL_TO_VALUE.get(option)) is None:
            raise HomeAssistantError(f"Unknown work mode: {option}")
        await self._async_write(value)
