"""The Hinen Solar integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import HinenApiClient
from .coordinator import HinenDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hinen Solar from a config entry."""
    session = async_get_clientsession(hass)

    api = HinenApiClient(
        session=session,
        client_id=entry.data["client_id"],
        client_secret=entry.data["client_secret"],
        region_code=entry.data["region_code"],
        access_token=entry.data.get("access_token"),
        refresh_token=entry.data.get("refresh_token"),
        host=entry.data.get("host"),
    )

    try:
        # Verify authentication by fetching devices
        await api.async_get_devices()
    except Exception as err:
        _LOGGER.error("Error communicating with API: %s", err)
        raise ConfigEntryNotReady from err

    coordinator = HinenDataUpdateCoordinator(hass, api)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
