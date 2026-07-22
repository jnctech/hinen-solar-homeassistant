"""Authenticated REST client for the Hinen Solar cloud API.

Token lifecycle lives in the OAuth2 layer (see ``oauth2.py``); this client asks
the supplied ``token_provider`` for a fresh ``(access_token, host)`` before every
request, so token refresh is transparent here and no credentials are stored on
the client itself.
"""
from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)

# Async callable returning the current (access_token, host) pair.
TokenProvider = Callable[[], Awaitable[tuple[str, str]]]

# Success code returned in the JSON body by the Hinen API.
API_SUCCESS_CODE = "00000"


class HinenApiError(Exception):
    """Raised when the Hinen API returns a non-success response body."""


class HinenApiClient:
    """Thin authenticated client for the Hinen device REST API."""

    def __init__(self, session: ClientSession, token_provider: TokenProvider) -> None:
        """Initialize the client with a session and a token provider."""
        self._session = session
        self._token_provider = token_provider

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        """Make an authenticated request and return the ``data`` payload."""
        access_token, host = await self._token_provider()
        url = f"{host}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = access_token

        async with self._session.request(
            method, url, headers=headers, **kwargs
        ) as response:
            response.raise_for_status()
            data = await response.json()

        if data.get("code") != API_SUCCESS_CODE:
            raise HinenApiError(
                f"Hinen API {method} {endpoint} failed "
                f"({data.get('code')}): {data.get('msg')}"
            )
        return data.get("data")

    async def async_get_devices(self) -> list[dict[str, Any]]:
        """Return the list of devices on the account."""
        return await self._request("GET", "/iot-device/open-api/devices")

    async def async_get_device_info(self, device_id: str) -> dict[str, Any]:
        """Return detailed device info, including the properties array."""
        return await self._request(
            "GET", f"/iot-device/open-api/devices/info/{device_id}"
        )

    async def async_set_device_property(
        self, device_id: str, properties: dict[str, Any]
    ) -> Any:
        """Set one or more writable device properties."""
        payload = {"deviceId": device_id, "map": properties}
        return await self._request(
            "PUT", "/iot-device/open-api/devices/property_set", json=payload
        )
