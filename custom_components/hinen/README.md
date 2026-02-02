# Hinen Solar Home Assistant Integration

A custom Home Assistant integration for Hinen solar inverters, PV systems, and battery storage using the celinksmart cloud platform.

## Features

- **OAuth2 Authentication**: Secure authentication with celinksmart API
- **Multi-Region Support**: Supports Europe, Asia-Pacific, and Australia data centers
- **Comprehensive Monitoring**:
  - PV panels (voltage, current, power for up to 4 strings)
  - Battery (SOC, voltage, current, temperature, power, capacity)
  - Grid (voltage, current, power, frequency)
  - Inverter (temperature, rated power)
  - Energy statistics (daily, monthly, yearly, total)
- **Binary Sensors**: Online status and battery charging state
- **Energy Dashboard Compatible**: Sensors work with Home Assistant's energy dashboard
- **HACS Ready**: Can be installed via HACS custom repositories

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add this repository URL and select "Integration" as the category
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/hinen` directory to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

### Prerequisites

Before configuring the integration, you need to obtain your developer credentials:

1. Contact Hinen technical support to get access to the developer platform
2. Log in to the [Hinen Developer Platform](https://developer.celinksmart.com)
3. Navigate to "Backend Management" > "Application List"
4. Copy your **Client ID** and **Client Secret**

### Setup

1. Go to **Settings** > **Devices & Services** in Home Assistant
2. Click **+ Add Integration**
3. Search for "Hinen Solar"
4. Enter your **Client ID**, **Client Secret**, and **Region Code**
5. Click **Submit**
6. You will be shown an authorization URL
7. Visit the URL in your browser and log in with your Hinen account
8. After authorizing, you will receive an **Authorization Code**
9. Enter the authorization code in Home Assistant
10. Click **Submit**

Your devices will now be added to Home Assistant!

## Sensors

### Power Monitoring
- **PV Generation Power**: Current solar panel power output
- **Battery Power**: Current battery charge/discharge power (positive = charging, negative = discharging)
- **Load Power**: Current power consumption
- **Grid Power**: Current grid import/export power (positive = importing, negative = exporting)
- **Total System Power**: Total system power generation

### Battery
- **Battery State of Charge (SOC)**: Battery charge level (%)
- **Battery Voltage**: Battery voltage (V)
- **Battery Current**: Battery current (A)
- **Battery Temperature**: Battery temperature (°C)
- **Battery Capacity**: Total battery capacity (Wh)

### PV Panels
- **PV1/PV2/PV3/PV4 Voltage**: Panel string voltages (V)
- **PV1/PV2/PV3/PV4 Current**: Panel string currents (A)
- **PV1/PV2/PV3/PV4 Power**: Panel string powers (W)

### Grid
- **Grid R/S/T-Phase Voltage**: Grid phase voltages (V)
- **Grid R/S/T-Phase Current**: Grid phase currents (A)
- **Grid R/S/T-Phase Power**: Grid phase powers (W)
- **Grid Frequency**: Grid frequency (Hz)

### Energy Statistics
- **Daily/Total Consumption**: Energy consumed by loads
- **Daily/Total Grid Feed-in**: Energy exported to grid
- **Daily/Total Energy Purchased**: Energy imported from grid
- **Daily/Total Charging Energy**: Energy charged to battery
- **Daily/Total Discharging Energy**: Energy discharged from battery

### Inverter
- **Inverter Temperature**: Inverter temperature (°C)
- **DC-DC Temperature**: DC-DC converter temperature (°C)
- **Rated Power**: Inverter rated power (W)

### Binary Sensors
- **Online Status**: Device connectivity status
- **Battery Charging**: Whether the battery is currently charging

## Energy Dashboard Configuration

The integration provides sensors compatible with Home Assistant's Energy Dashboard:

1. Go to **Settings** > **Dashboards** > **Energy**
2. Configure your energy sources:
   - **Solar Production**: Use `sensor.hinen_pv_generation_power`
   - **Battery Storage**: Use `sensor.hinen_battery_power`
   - **Grid Consumption**: Use `sensor.hinen_daily_energy_purchased`
   - **Return to Grid**: Use `sensor.hinen_daily_grid_feed_in`

## Supported Regions

The integration supports the following regions:

### Europe
Austria (AT), Belgium (BE), Switzerland (CH), Czech Republic (CZ), Germany (DE), Denmark (DK), Spain (ES), Finland (FI), France (FR), United Kingdom (GB), Greece (GR), Ireland (IE), Italy (IT), Netherlands (NL), Poland (PL), Portugal (PT), Sweden (SE), and more

### Asia Pacific
Singapore (SG), Pakistan (PK)

### Australia
Australia (AU), New Zealand (NZ)

## Troubleshooting

### Authentication Failed
- Verify your Client ID and Client Secret are correct
- Ensure you copied the authorization code correctly
- Check that your Hinen account has access to the devices

### No Devices Found
- Log in to the Hinen mobile app to verify your devices are registered
- Contact Hinen support to ensure your account has proper device access

### Sensors Not Updating
- Check your internet connection
- Verify the integration is not showing as "Unavailable" in Settings > Devices & Services
- Try reloading the integration

## API Rate Limits

The celinksmart API has the following rate limits:
- Default: 2500 requests per 5 minutes
- Contact Hinen technical support if you need higher limits

## Support

For issues and feature requests, please open an issue on GitHub.

## License

This integration is provided as-is for use with Hinen solar equipment.

## Credits

Developed for the Home Assistant community.
