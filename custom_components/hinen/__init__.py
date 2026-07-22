"""The Hinen Solar integration."""

from __future__ import annotations

import logging

from aiohttp import ClientError, ClientResponseError
from homeassistant.components.application_credentials import ClientCredential
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_TOKEN, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import application_credentials
from .api import HinenApiClient
from .const import DOMAIN, TOKEN_CLIENT_ID, TOKEN_CLIENT_SECRET
from .coordinator import HinenDataUpdateCoordinator
from .oauth2 import HinenConfigEntryAuth

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hinen Solar from a config entry."""
    token = entry.data[CONF_TOKEN]
    credential = ClientCredential(token[TOKEN_CLIENT_ID], token[TOKEN_CLIENT_SECRET])
    implementation = await application_credentials.async_get_auth_implementation(hass, DOMAIN, credential)
    config_entry_oauth2_flow.async_register_implementation(hass, DOMAIN, implementation)

    impl = await config_entry_oauth2_flow.async_get_config_entry_implementation(hass, entry)
    oauth_session = config_entry_oauth2_flow.OAuth2Session(hass, entry, impl)
    auth = HinenConfigEntryAuth(oauth_session)

    try:
        await auth.check_and_refresh_token()
    except ClientResponseError as err:
        if 400 <= err.status < 500:
            raise ConfigEntryAuthFailed("Hinen token is no longer valid; reauthentication required") from err
        raise ConfigEntryNotReady from err
    except ClientError as err:
        raise ConfigEntryNotReady from err

    client = HinenApiClient(async_get_clientsession(hass), auth.async_get_token_and_host)
    coordinator = HinenDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
