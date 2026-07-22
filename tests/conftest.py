"""Shared fixtures and sample API payloads for the Hinen tests.

Payloads mirror the real Hinen cloud API shapes so the tests exercise the actual
parsing/normalisation paths — no MagicMock stand-ins. Identifiers (device id and
serial number) are synthetic placeholders, not real hardware.
"""

from __future__ import annotations

import time
from collections.abc import Generator

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hinen.const import DOMAIN

# --- Endpoint constants (must match const.py / api.py) ------------------------
HOST = "https://au.iot-api.celinksmart.com"
DEVICES_URL = f"{HOST}/iot-device/open-api/devices"
DEVICE_ID = "1000000000000000001"
DEVICE_INFO_URL = f"{HOST}/iot-device/open-api/devices/info/{DEVICE_ID}"
PROPERTY_SET_URL = f"{HOST}/iot-device/open-api/devices/property_set"

# --- Stored OAuth token (as persisted in the config entry) --------------------
STORED_TOKEN = {
    "access_token": "access-token-1",
    "refresh_token": "refresh-token-1",
    "expires_in": 3600,
    # Far-future so OAuth2Session.async_ensure_token_valid never refreshes in tests
    # that don't specifically exercise refresh.
    "expires_at": time.time() + 3600,
    "host": HOST,
    "region_code": "AU",
    "client_id": "client-id-1",
    "client_secret": "client-secret-1",
}

# --- Raw API responses --------------------------------------------------------
TOKEN_RESPONSE = {
    "code": "00000",
    "msg": "Request succeeded",
    "data": {
        "accessToken": "access-token-1",
        "refreshToken": "refresh-token-1",
        "host": HOST,
        "expiresIn": 3600,
    },
}

DEVICES_RESPONSE = {
    "code": "00000",
    "msg": "Request succeeded",
    "data": [
        {
            "id": DEVICE_ID,
            "deviceName": "Single-phase Hybrid Inverter",
            "serialNumber": "HTEST0000000000000001",
            "modelCode": "SH6KL-SG1-EU",
            "firmwareVersion": "2.1.24",
            "status": 1,
            "alertStatus": 0,
        }
    ],
}

DEVICE_INFO_RESPONSE = {
    "code": "00000",
    "msg": "Request succeeded",
    "data": {
        "deviceName": "Single-phase Hybrid Inverter",
        "serialNumber": "HTEST0000000000000001",
        "modelCode": "SH6KL-SG1-EU",
        "firmwareVersion": "2.1.24",
        "status": 1,
        "alertStatus": 0,
        "properties": [
            {"identifier": "Pv1Power", "name": "PV1 Power", "value": 565.8, "specs": {"unit": "W"}},
            {"identifier": "Pv2Power", "name": "PV2 Power", "value": 372.1, "specs": {"unit": "W"}},
            {"identifier": "PmeterPV", "name": "PV Meter Total", "value": 701.6, "specs": {"unit": "W"}},
            {"identifier": "GenerationPower", "name": "Generation Power", "value": 1679, "specs": {"unit": "W"}},
            {"identifier": "BatteryPower", "name": "Battery Power", "value": 1074, "specs": {"unit": "W"}},
            {"identifier": "SOC", "name": "SOC", "value": 28, "specs": {"unit": "%"}},
            {"identifier": "SOH", "name": "SOH", "value": 96, "specs": {"unit": "%"}},
            {
                "identifier": "CumulativeProductionActive",
                "name": "Total Yield",
                "value": 13591.3,
                "specs": {"unit": "kWh"},
            },
            {"identifier": "TotalLoadPower", "name": "Load Power", "value": 649, "specs": {"unit": "W"}},
            {
                "identifier": "ChargeStopSOC",
                "name": "Forced Charge Cutoff SOC",
                "value": 70,
                "shadow": 70,
                "datatype": "integer",
                "specs": {"unit": "%", "min": 10, "max": 100, "step": 1},
            },
            {
                "identifier": "WorkModeSetting",
                "name": "Work Mode Setting",
                "value": 10,
                "shadow": 10,
                "datatype": "enum",
                "specs": {"enumList": [{"text": "self", "value": 10}]},
            },
        ],
    },
}


def error_response(code: str = "A0400", msg: str = "bad request") -> dict:
    """Build a non-success API body."""
    return {"code": code, "msg": msg, "data": None}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None, None, None]:
    """Enable loading of the custom integration in every test."""
    yield


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """A config entry with a valid stored OAuth token."""
    return MockConfigEntry(
        domain=DOMAIN,
        unique_id=DEVICE_ID,
        title="Single-phase Hybrid Inverter",
        data={"auth_implementation": DOMAIN, "token": dict(STORED_TOKEN)},
    )
