"""Config flow for the Hinen Solar integration."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant.components.application_credentials import ClientCredential
from homeassistant.config_entries import SOURCE_REAUTH, SOURCE_RECONFIGURE, ConfigFlowResult
from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET, CONF_TOKEN
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import application_credentials
from .api import HinenApiClient
from .const import (
    CONF_AUTH_LANGUAGE,
    CONF_REDIRECT_BASE,
    DEVELOPER_PORTAL_URL,
    DOMAIN,
    SUPPORTED_LANGUAGES,
    TOKEN_HOST,
)
from .oauth2 import HinenOAuth2CallbackView

_LOGGER = logging.getLogger(__name__)


class HinenOAuth2FlowHandler(config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN):
    """Handle the Hinen Solar OAuth2 config flow."""

    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return the logger for the flow."""
        return _LOGGER

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Collect credentials, then hand off to the OAuth authorize step."""
        if user_input is not None:
            credential = ClientCredential(user_input[CONF_CLIENT_ID], user_input[CONF_CLIENT_SECRET])
            implementation = await application_credentials.async_get_auth_implementation(self.hass, DOMAIN, credential)
            implementation.auth_language = user_input[CONF_AUTH_LANGUAGE]
            implementation.redirect_base = user_input[CONF_REDIRECT_BASE]

            self.hass.http.register_view(HinenOAuth2CallbackView())
            self.flow_impl = implementation
            config_entry_oauth2_flow.async_register_implementation(self.hass, DOMAIN, implementation)
            return await self.async_step_auth()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_AUTH_LANGUAGE, default="en_US"): vol.In(SUPPORTED_LANGUAGES),
                    vol.Required(CONF_CLIENT_ID): str,
                    vol.Required(CONF_CLIENT_SECRET): str,
                    vol.Required(
                        CONF_REDIRECT_BASE,
                        default="http://homeassistant.local:8123",
                    ): str,
                }
            ),
            description_placeholders={"portal_url": DEVELOPER_PORTAL_URL},
        )

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> ConfigFlowResult:
        """Verify the token works against the account, then create/update the entry."""
        token = data[CONF_TOKEN]
        session = async_get_clientsession(self.hass)

        async def _token_provider() -> tuple[str, str]:
            return token["access_token"], token[TOKEN_HOST]

        client = HinenApiClient(session, _token_provider)
        try:
            devices = await client.async_get_devices()
        except Exception as err:  # noqa: BLE001 - surfaced as an abort reason
            _LOGGER.error("Error verifying Hinen devices: %s", err)
            return self.async_abort(reason="cannot_connect")

        if not devices:
            return self.async_abort(reason="no_devices")

        await self.async_set_unique_id(str(devices[0]["id"]))
        if self.source == SOURCE_REAUTH:
            self._abort_if_unique_id_mismatch(reason="wrong_account")
            return self.async_update_reload_and_abort(self._get_reauth_entry(), data=data)
        if self.source == SOURCE_RECONFIGURE:
            self._abort_if_unique_id_mismatch(reason="wrong_account")
            return self.async_update_reload_and_abort(self._get_reconfigure_entry(), data=data)
        self._abort_if_unique_id_configured()
        title = devices[0].get("deviceName") or "Hinen Solar Advanced"
        return self.async_create_entry(title=title, data=data)

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Re-enter credentials without waiting for the token to fail.

        Reauth only becomes reachable once the stored token is rejected, which is
        too late when the credentials are rotated deliberately — the entry still
        holds the old client id and secret while the current access token keeps
        working. This gives a path to update them on demand.
        """
        return await self.async_step_user()

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> ConfigFlowResult:
        """Handle re-authentication when the stored token becomes invalid."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Confirm re-authentication, then restart the credential step."""
        if user_input is None:
            return self.async_show_form(step_id="reauth_confirm")
        return await self.async_step_user()
