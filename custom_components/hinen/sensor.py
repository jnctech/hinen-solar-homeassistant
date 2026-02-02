"""Sensor platform for Hinen Solar."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HinenDataUpdateCoordinator


@dataclass
class HinenSensorEntityDescription(SensorEntityDescription):
    """Describes Hinen sensor entity."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None


SENSOR_DESCRIPTIONS: tuple[HinenSensorEntityDescription, ...] = (
    # PV Sensors
    HinenSensorEntityDescription(
        key="Pv1Voltage",
        name="PV1 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="Pv1Current",
        name="PV1 Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="Pv1Power",
        name="PV1 Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="Pv2Voltage",
        name="PV2 Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="Pv2Current",
        name="PV2 Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="Pv2Power",
        name="PV2 Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Grid Sensors
    HinenSensorEntityDescription(
        key="RVoltage",
        name="Grid R-Phase Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="RCurrent",
        name="Grid R-Phase Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="RPower",
        name="Grid R-Phase Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="Frequency",
        name="Grid Frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Power Sensors
    HinenSensorEntityDescription(
        key="SystemProductionTotalPower",
        name="Total System Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="TotalActivePower",
        name="Total Active Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="BatteryPower",
        name="Battery Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="GenerationPower",
        name="PV Generation Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="TotalLoadPower",
        name="Load Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="GridTotalPower",
        name="Grid Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Battery Sensors
    HinenSensorEntityDescription(
        key="BatteryVoltage",
        name="Battery Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="BatteryCurrent",
        name="Battery Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="BatteryTemperature",
        name="Battery Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="SOC",
        name="Battery State of Charge",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="BatCapacity",
        name="Battery Capacity",
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Inverter Temperature Sensors
    HinenSensorEntityDescription(
        key="InvTemp",
        name="Inverter Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    HinenSensorEntityDescription(
        key="DcdcTemp",
        name="DC-DC Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Energy Statistics (Total)
    HinenSensorEntityDescription(
        key="CumulativeConsumption",
        name="Total Consumption",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="CumulativeGridFeedIn",
        name="Total Grid Feed-in",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="CumulativeEnergyPurchased",
        name="Total Energy Purchased",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="TotalChargingEnergy",
        name="Total Charging Energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="TotalDischargingEnergy",
        name="Total Discharging Energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Energy Statistics (Daily)
    HinenSensorEntityDescription(
        key="DailyConsumption",
        name="Daily Consumption",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyGridFeedIn",
        name="Daily Grid Feed-in",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyEnergyPurchased",
        name="Daily Energy Purchased",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyChargingEnergy",
        name="Daily Charging Energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyDischargingEnergy",
        name="Daily Discharging Energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Device Info
    HinenSensorEntityDescription(
        key="RatedPower",
        name="Rated Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hinen Solar sensor based on a config entry."""
    coordinator: HinenDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[HinenSensor] = []

    # Create sensors for each device
    for device_id in coordinator.devices:
        for description in SENSOR_DESCRIPTIONS:
            entities.append(HinenSensor(coordinator, device_id, description))

    async_add_entities(entities)


class HinenSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Hinen Solar sensor."""

    entity_description: HinenSensorEntityDescription

    def __init__(
        self,
        coordinator: HinenDataUpdateCoordinator,
        device_id: str,
        description: HinenSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_id = device_id

        device_name = coordinator.get_device_name(device_id)
        self._attr_name = f"{device_name} {description.name}"
        self._attr_unique_id = f"{device_id}_{description.key}"

        # Set device info
        device_data = coordinator.devices.get(device_id, {})
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device_name,
            "manufacturer": "Hinen",
            "model": device_data.get("model_code", "Solar Inverter"),
            "sw_version": device_data.get("firmware_version"),
            "serial_number": device_data.get("serial_number"),
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        value = self.coordinator.get_device_property(
            self._device_id, self.entity_description.key
        )

        # Return None if value doesn't exist
        if value is None:
            return None

        # Apply custom value function if defined
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(value)

        return value

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not super().available:
            return False

        # Check if the device exists in coordinator data
        return self._device_id in self.coordinator.devices
