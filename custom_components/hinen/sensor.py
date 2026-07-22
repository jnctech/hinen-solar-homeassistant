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
    # External / metered PV generation (e.g. an AC-coupled inverter such as a
    # Solis measured by the Hinen PV meter). GenerationPower = PV1+PV2 + this.
    HinenSensorEntityDescription(
        key="PmeterPV",
        name="PV Meter Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="PVPercentPower",
        name="PV Output Percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Power-flow matrix (instantaneous routing between PV / grid / battery / load)
    HinenSensorEntityDescription(
        key="PvToBatteryPower",
        name="PV to Battery Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="PvToLoadPower",
        name="PV to Load Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="PvToGridPower",
        name="PV to Grid Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="GridToLoadPower",
        name="Grid to Load Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="GridToBatteryPower",
        name="Grid to Battery Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="BatteryToLoadPower",
        name="Battery to Load Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HinenSensorEntityDescription(
        key="BatteryToGridPower",
        name="Battery to Grid Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # PV-routing energy — Daily (resets at midnight) and lifetime Total.
    HinenSensorEntityDescription(
        key="DailyPvToLoadEnergy",
        name="Daily PV to Load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyPvToGridEnergy",
        name="Daily PV to Grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyPvToBatteryEnergy",
        name="Daily PV to Battery",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # NB: identifier "TotalPvToLoadPower" is a Hinen misnomer — it is cumulative
    # energy in kWh (name: "Total PV energy supplied to the load"), not power.
    HinenSensorEntityDescription(
        key="TotalPvToLoadPower",
        name="Total PV to Load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="TotalPvToGridEnergy",
        name="Total PV to Grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="TotalPvToBatteryEnergy",
        name="Total PV to Battery",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Total solar yield — THE "Solar production" figure for the Energy Dashboard.
    # Matches the Hinen app headline "yield"; CumulativeProductionActive spans the
    # whole array incl. the external Solis's full history (hence >> the PvTo* sums).
    HinenSensorEntityDescription(
        key="DailyProductionActive",
        name="Daily Yield",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="CumulativeProductionActive",
        name="Total Yield",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Energy-flow matrix — Daily + lifetime Total (completes the PvTo* set above).
    HinenSensorEntityDescription(
        key="DailyGridToLoadEnergy",
        name="Daily Grid to Load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="TotalGridToLoadEnergy",
        name="Total Grid to Load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyGridToBatteryEnergy",
        name="Daily Grid to Battery",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="TotalGridToBatteryEnergy",
        name="Total Grid to Battery",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyBatteryToLoadEnergy",
        name="Daily Battery to Load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="TotalBatteryToLoadEnergy",
        name="Total Battery to Load",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="DailyBatteryToGridEnergy",
        name="Daily Battery to Grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    HinenSensorEntityDescription(
        key="TotalBatteryToGridEnergy",
        name="Total Battery to Grid",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Battery health & cell diagnostics
    HinenSensorEntityDescription(
        key="SOH",
        name="Battery Health",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    HinenSensorEntityDescription(
        key="NumberOfBatteriesInParallel",
        name="Battery Pack Quantity",
        native_unit_of_measurement="packs",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    HinenSensorEntityDescription(
        key="HighestMonomerVoltage",
        name="Battery Cell Max Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    HinenSensorEntityDescription(
        key="LowestMonomerVoltage",
        name="Battery Cell Min Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    HinenSensorEntityDescription(
        key="BatteryCellMaxTemperature",
        name="Battery Cell Max Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    HinenSensorEntityDescription(
        key="BatteryCellMinTemperature",
        name="Battery Cell Min Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    HinenSensorEntityDescription(
        key="IsoResistance",
        name="ISO Resistance",
        native_unit_of_measurement="kΩ",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    HinenSensorEntityDescription(
        key="PowerFactor",
        name="Power Factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
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

        # Set device info with unique identifier to avoid conflicts with official integration
        device_data = coordinator.devices.get(device_id, {})
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{device_id}_advanced")},
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
