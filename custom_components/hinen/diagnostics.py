"""Diagnostics support for Hinen Solar."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from .coordinator import HinenConfigEntry

# OAuth material plus anything that identifies the specific hardware or account.
# Diagnostics downloads routinely get pasted into public issue reports, so the
# device id and serial number are redacted alongside the credentials.
TO_REDACT = {
    "access_token",
    "refresh_token",
    "client_id",
    "client_secret",
    "id",
    "serial_number",
}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: HinenConfigEntry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry": {
            "title": entry.title,
            "data": async_redact_data(entry.data, TO_REDACT),
        },
        "last_update_success": coordinator.last_update_success,
        # coordinator.devices is keyed by device id; emit the values only, since
        # redaction rewrites values and would leave the ids exposed as keys.
        "devices": [async_redact_data(device, TO_REDACT) for device in coordinator.devices.values()],
    }
