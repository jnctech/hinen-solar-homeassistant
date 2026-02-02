"""API client for Hinen Solar."""
from __future__ import annotations

import logging
from typing import Any
from datetime import datetime, timedelta

import aiohttp
from aiohttp import ClientSession, ClientResponseError

from .const import (
    GRANT_TYPE_AUTHORIZATION_CODE,
    GRANT_TYPE_REFRESH_TOKEN,
    OAUTH_TOKEN_URL,
)

_LOGGER = logging.getLogger(__name__)


class HinenApiClient:
    """API client for Hinen Solar."""

    def __init__(
        self,
        session: ClientSession,
        client_id: str,
        client_secret: str,
        region_code: str,
        access_token: str | None = None,
        refresh_token: str | None = None,
        host: str | None = None,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._client_id = client_id
        self._client_secret = client_secret
        self._region_code = region_code
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._host = host
        self._token_expiration: datetime | None = None

    async def async_get_access_token(
        self, authorization_code: str
    ) -> dict[str, Any]:
        """Get access token using authorization code."""
        params = {
            "clientSecret": self._client_secret,
            "grantType": GRANT_TYPE_AUTHORIZATION_CODE,
            "regionCode": self._region_code,
            "authorizationCode": authorization_code,
        }

        async with self._session.get(
            OAUTH_TOKEN_URL, params=params
        ) as response:
            response.raise_for_status()
            data = await response.json()

            if data.get("code") != "00000":
                raise Exception(f"Token request failed: {data.get('msg')}")

            token_data = data["data"]
            self._access_token = token_data["accessToken"]
            self._refresh_token = token_data["refreshToken"]
            self._host = token_data["host"]

            # Set expiration time
            expires_in = token_data.get("expiresIn", 3600)
            self._token_expiration = datetime.now() + timedelta(seconds=expires_in - 300)  # 5 min buffer

            return {
                "access_token": self._access_token,
                "refresh_token": self._refresh_token,
                "host": self._host,
            }

    async def async_refresh_access_token(self) -> dict[str, Any]:
        """Refresh the access token."""
        if not self._refresh_token:
            raise Exception("No refresh token available")

        params = {
            "clientSecret": self._client_secret,
            "grantType": GRANT_TYPE_REFRESH_TOKEN,
            "regionCode": self._region_code,
            "refreshToken": self._refresh_token,
        }

        async with self._session.get(
            OAUTH_TOKEN_URL, params=params
        ) as response:
            response.raise_for_status()
            data = await response.json()

            if data.get("code") != "00000":
                raise Exception(f"Token refresh failed: {data.get('msg')}")

            token_data = data["data"]
            self._access_token = token_data["accessToken"]
            self._refresh_token = token_data["refreshToken"]
            self._host = token_data["host"]

            # Set expiration time
            expires_in = token_data.get("expiresIn", 3600)
            self._token_expiration = datetime.now() + timedelta(seconds=expires_in - 300)

            return {
                "access_token": self._access_token,
                "refresh_token": self._refresh_token,
                "host": self._host,
            }

    async def _ensure_valid_token(self) -> None:
        """Ensure we have a valid access token."""
        if self._token_expiration and datetime.now() >= self._token_expiration:
            _LOGGER.debug("Token expired, refreshing...")
            await self.async_refresh_access_token()

    async def _async_request(
        self, method: str, endpoint: str, **kwargs
    ) -> dict[str, Any]:
        """Make an authenticated API request."""
        await self._ensure_valid_token()

        if not self._host or not self._access_token:
            raise Exception("Not authenticated")

        url = f"{self._host}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = self._access_token

        async with self._session.request(
            method, url, headers=headers, **kwargs
        ) as response:
            response.raise_for_status()
            data = await response.json()

            if data.get("code") != "00000":
                raise Exception(f"API request failed: {data.get('msg')}")

            return data.get("data")

    async def async_get_devices(self) -> list[dict[str, Any]]:
        """Get list of devices."""
        return await self._async_request(
            "GET", "/iot-device/open-api/devices"
        )

    async def async_get_device_info(self, device_id: str) -> dict[str, Any]:
        """Get detailed device information including properties."""
        return await self._async_request(
            "GET", f"/iot-device/open-api/devices/info/{device_id}"
        )

    async def async_set_device_property(
        self, device_id: str, properties: dict[str, Any]
    ) -> dict[str, Any]:
        """Set device properties."""
        payload = {"deviceId": device_id, "map": properties}
        return await self._async_request(
            "PUT", "/iot-device/open-api/devices/property_set", json=payload
        )
