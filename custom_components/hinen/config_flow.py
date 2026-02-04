"""Config flow for Hinen Solar integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.network import get_url

from .api import HinenApiClient
from .auth_callback import async_register_callback_view
from .const import DOMAIN, OAUTH_AUTHORIZE_URL

_LOGGER = logging.getLogger(__name__)

# Region options
REGIONS = {
    "AU": "Australia",
    "NZ": "New Zealand",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "ES": "Spain",
    "IT": "Italy",
    "NL": "Netherlands",
    "BE": "Belgium",
    "PL": "Poland",
    "SE": "Sweden",
    "AT": "Austria",
    "CH": "Switzerland",
    "PT": "Portugal",
    "IE": "Ireland",
    "DK": "Denmark",
    "FI": "Finland",
    "NO": "Norway",
    "GR": "Greece",
    "CZ": "Czech Republic",
    "SG": "Singapore",
    "PK": "Pakistan",
}


class HinenConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hinen Solar."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._client_id: str | None = None
        self._client_secret: str | None = None
        self._region_code: str | None = None
        self._auth_code: str | None = None
        self._redirect_url: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        # Check for conflict with official Hinen Power integration
        for entry in self.hass.config_entries.async_entries():
            if entry.domain == "hinen_power":
                return self.async_abort(
                    reason="conflict_with_official",
                    description_placeholders={
                        "integration_name": "Hinen Power",
                    },
                )

        # Register the OAuth callback view
        async_register_callback_view(self.hass)

        if user_input is not None:
            self._client_id = user_input["client_id"]
            self._client_secret = user_input["client_secret"]
            self._region_code = user_input["region_code"]
            self._redirect_url = user_input.get("redirect_url")

            # Generate OAuth URL for user to authorize
            # redirectUrl parameter is required for all regions
            auth_url = f"{OAUTH_AUTHORIZE_URL}?language=en_US&key={self._client_id}&state=homeassistant&redirectUrl={self._redirect_url}"

            return self.async_show_form(
                step_id="authorize",
                data_schema=vol.Schema(
                    {
                        vol.Optional("authorization_code", default=""): str,
                    }
                ),
                description_placeholders={
                    "auth_url": auth_url,
                    "redirect_url": self._redirect_url,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("client_id"): str,
                    vol.Required("client_secret"): str,
                    vol.Required("region_code"): vol.In(REGIONS),
                    vol.Optional(
                        "redirect_url",
                        default="http://homeassistant.local:8123/api/hinen_solar/oauth/callback",
                    ): str,
                }
            ),
            errors=errors,
        )

    async def async_step_authorize(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the authorization step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            auth_code = user_input.get("authorization_code", "").strip()

            # Check if callback received the code (when user submits empty form)
            if not auth_code and DOMAIN in self.hass.data:
                callback_data = self.hass.data[DOMAIN].get("oauth_callback")
                if callback_data and "authorization_code" in callback_data:
                    auth_code = callback_data["authorization_code"]
                    # Clear the callback data
                    self.hass.data[DOMAIN].pop("oauth_callback", None)
                    _LOGGER.info("Using authorization code from OAuth callback")

            if not auth_code:
                errors["base"] = "auth_failed"
                errors["authorization_code"] = "Please enter the authorization code or complete the OAuth flow"
            else:
                session = async_get_clientsession(self.hass)
                api = HinenApiClient(
                    session=session,
                    client_id=self._client_id,
                    client_secret=self._client_secret,
                    region_code=self._region_code,
                )

                try:
                    # Exchange authorization code for tokens
                    token_data = await api.async_get_access_token(auth_code)

                    # Verify by fetching devices
                    devices = await api.async_get_devices()

                    if not devices:
                        errors["base"] = "no_devices"
                    else:
                        # Create config entry
                        return self.async_create_entry(
                            title=f"Hinen Solar Advanced ({self._region_code})",
                            data={
                                "client_id": self._client_id,
                                "client_secret": self._client_secret,
                                "region_code": self._region_code,
                                "access_token": token_data["access_token"],
                                "refresh_token": token_data["refresh_token"],
                                "host": token_data["host"],
                            },
                        )

                except Exception as err:
                    _LOGGER.error("Error during authorization: %s", err)
                    errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="authorize",
            data_schema=vol.Schema(
                {
                    vol.Optional("authorization_code", default=""): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return HinenOptionsFlowHandler(config_entry)


class HinenOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Hinen Solar."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "scan_interval",
                        default=self.config_entry.options.get("scan_interval", 60),
                    ): vol.All(vol.Coerce(int), vol.Range(min=30, max=300)),
                }
            ),
        )
