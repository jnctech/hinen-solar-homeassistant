# Hinen Solar Advanced - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/v/release/jnctech/hinen-solar-homeassistant)](https://github.com/jnctech/hinen-solar-homeassistant/releases)
[![License](https://img.shields.io/github/license/jnctech/hinen-solar-homeassistant.svg)](LICENSE)

> **🚀 Release Candidate 3:** This is version 1.0.0-rc3. **NEW:** Automatic OAuth redirect + conflict detection with official Hinen Power integration.

**Advanced monitoring integration** for Hinen solar inverters, PV systems, and battery storage. Provides **35+ detailed sensors** for power users who want comprehensive monitoring beyond the official integration.

> **⚠️ COMPATIBILITY NOTICE:** This integration **cannot run simultaneously** with the [official Hinen Power integration](https://github.com/Hinen-IoT/ha_hinen_power) on the same Hinen account due to API session limitations. See [Compatibility](#compatibility) section below for details and workarounds.

## Why Use This Integration?

**Official Hinen Power Integration:**
- ✅ 12 basic sensors
- ✅ Control features (work modes, charge/discharge settings)
- ✅ Simple setup

**Hinen Solar Advanced (This Integration):**
- ✅ **35+ sensors** - 3x more monitoring data
- ✅ **PV String Monitoring** - Track each of your 4 solar panel strings individually
- ✅ **3-Phase Grid Monitoring** - Essential for commercial installations
- ✅ **Battery Health** - Voltage, current, temperature tracking
- ✅ **Detailed Energy Statistics** - Daily, monthly, yearly breakdowns
- ✅ Advanced monitoring for power users and solar enthusiasts

## Compatibility

### ⚠️ Cannot Run with Official Hinen Power Integration

**Important:** This integration **cannot run simultaneously** with the [official Hinen Power integration](https://github.com/Hinen-IoT/ha_hinen_power) when using the **same Hinen account**.

**Why?** The Hinen API enforces session limitations that prevent multiple integrations from accessing the same account concurrently. When both are installed:
- One integration will show "Device Unavailable" or "Couldn't connect" errors
- API requests from one integration may invalidate the other's session
- Only one integration can reliably update at a time

**Note:** The Hinen mobile app CAN run alongside either integration (mobile apps use different API endpoints).

### Workarounds

**Option 1: Choose One Integration**
- Use **Hinen Solar Advanced** if you want detailed monitoring (35+ sensors)
- Use **Hinen Power** if you need control features (changing modes, settings)

**Option 2: Use Separate Hinen Accounts** (Advanced Users)
- Create a second Hinen account
- Share your solar devices to the second account (if supported by Hinen)
- Use one account for Hinen Power, another for Hinen Solar Advanced

**Future:** We're working on resolving this limitation by using the same underlying API library as the official integration. Track progress in [Issue #2](https://github.com/jnctech/hinen-solar-homeassistant/issues/2).

### Installation will be blocked if official integration is detected

The integration will automatically detect if Hinen Power is installed and prevent installation to avoid conflicts. If you want to use Hinen Solar Advanced, remove Hinen Power first.

## Features

- 📊 **35+ Sensors**: Comprehensive monitoring of solar, battery, grid, and load
- ☀️ **PV String Monitoring**: Up to 4 PV strings with voltage, current, and power
- ⚡ **3-Phase Grid Monitoring**: Voltage, current, power, and frequency per phase
- 🔋 **Battery Health**: SOC, voltage, current, temperature, charging state
- 📈 **Energy Statistics**: Daily, monthly, yearly, and total energy tracking
- 🏠 **Energy Dashboard**: Full compatibility with Home Assistant energy dashboard
- 🌍 **Multi-Region Support**: Europe, Asia-Pacific, and Australia data centers
- 🔄 **Automatic Token Refresh**: Seamless re-authentication
- ✅ **OAuth2 Authentication**: Secure cloud authentication

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots (⋮) in the top right
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/jnctech/hinen-solar-homeassistant`
6. Select category: "Integration"
7. Click "Add"
8. Find "Hinen Solar" in HACS and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Download the latest release
2. Copy the `custom_components/hinen` folder to your `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

### Prerequisites

1. **Developer Credentials**:
   - Contact Hinen technical support to request developer platform access
   - Log in to [Hinen Developer Platform](https://developer.celinksmart.com)
   - Navigate to: Backend Management → Application List
   - Copy your **Client ID** and **Client Secret**

2. **Hinen Account**: Active account with registered solar devices

3. **Your Region**: Know your region code (e.g., AU, GB, DE, SG) - see [supported regions](#supported-regions)

### Setup Steps

1. In Home Assistant, go to: **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Hinen Solar Advanced"**
4. Enter your credentials:
   - **Client ID** from the developer platform
   - **Client Secret** from the developer platform
   - **Region** (e.g., AU for Australia)
5. Click **Submit**
6. Follow the **OAuth authorization link** shown
7. Sign in with your **Hinen account** credentials
8. Authorize the application
9. Copy the **authorization code** you receive
10. Paste it back into Home Assistant
11. Click **Submit**

Your 35+ sensors will appear automatically!

## Sensors

### Power Sensors
| Sensor | Description | Unit |
|--------|-------------|------|
| PV Generation Power | Current solar output | W |
| Battery Power | Charge/discharge power | W |
| Load Power | Current consumption | W |
| Grid Power | Import/export power | W |
| Total System Power | Total generation | W |

### Battery Sensors
| Sensor | Description | Unit |
|--------|-------------|------|
| Battery SOC | State of charge | % |
| Battery Voltage | Battery voltage | V |
| Battery Current | Charge/discharge current | A |
| Battery Temperature | Battery temperature | °C |
| Battery Capacity | Total capacity | Wh |

### PV String Sensors (×4)
| Sensor | Description | Unit |
|--------|-------------|------|
| PV1-4 Voltage | String voltage | V |
| PV1-4 Current | String current | A |
| PV1-4 Power | String power | W |

### Grid Sensors (3-Phase)
| Sensor | Description | Unit |
|--------|-------------|------|
| R/S/T Phase Voltage | Phase voltage | V |
| R/S/T Phase Current | Phase current | A |
| R/S/T Phase Power | Phase power | W |
| Grid Frequency | Frequency | Hz |

### Energy Statistics
| Sensor | Description | Unit |
|--------|-------------|------|
| Daily/Total Consumption | Load consumption | kWh |
| Daily/Total Grid Feed-in | Export to grid | kWh |
| Daily/Total Energy Purchased | Import from grid | kWh |
| Daily/Total Charging Energy | Battery charge | kWh |
| Daily/Total Discharging Energy | Battery discharge | kWh |

### Binary Sensors
| Sensor | Description |
|--------|-------------|
| Online Status | Device connectivity |
| Battery Charging | Charging state |

## Energy Dashboard Setup

Configure the Energy Dashboard (**Settings** → **Dashboards** → **Energy**):

- **Solar Production**: `sensor.{device}_pv_generation_power`
- **Battery Storage**: `sensor.{device}_battery_power`
- **Grid Consumption**: `sensor.{device}_daily_energy_purchased`
- **Return to Grid**: `sensor.{device}_daily_grid_feed_in`

## Supported Regions

### Europe (EU Data Center)
🇦🇹 Austria (AT) | 🇧🇪 Belgium (BE) | 🇧🇬 Bulgaria (BG) | 🇨🇭 Switzerland (CH) | 🇨🇾 Cyprus (CY) | 🇨🇿 Czech Republic (CZ) | 🇩🇪 Germany (DE) | 🇩🇰 Denmark (DK) | 🇪🇪 Estonia (EE) | 🇪🇸 Spain (ES) | 🇫🇮 Finland (FI) | 🇫🇷 France (FR) | 🇬🇧 United Kingdom (GB) | 🇬🇷 Greece (GR) | 🇭🇷 Croatia (HR) | 🇭🇺 Hungary (HU) | 🇮🇪 Ireland (IE) | 🇮🇹 Italy (IT) | 🇱🇹 Lithuania (LT) | 🇱🇺 Luxembourg (LU) | 🇱🇻 Latvia (LV) | 🇲🇹 Malta (MT) | 🇳🇱 Netherlands (NL) | 🇵🇱 Poland (PL) | 🇵🇹 Portugal (PT) | 🇷🇴 Romania (RO) | 🇸🇪 Sweden (SE) | 🇸🇮 Slovenia (SI) | 🇸🇰 Slovakia (SK) | 🇺🇦 Ukraine (UA)

### Asia-Pacific (AP Data Center)
🇸🇬 Singapore (SG) | 🇵🇰 Pakistan (PK)

### Australia (AU Data Center)
🇦🇺 Australia (AU) | 🇳🇿 New Zealand (NZ)

## Troubleshooting

### Authentication Failed
- ✅ Verify Client ID and Client Secret
- ✅ Check authorization code (ensure no extra spaces)
- ✅ Confirm your account has device access

### No Devices Found
- ✅ Log in to Hinen mobile app to verify device registration
- ✅ Contact Hinen support for account access verification

### Sensors Not Updating
- ✅ Check internet connectivity
- ✅ Verify integration status in Settings → Devices & Services
- ✅ Try reloading the integration
- ✅ Check Home Assistant logs for errors

### Token Expired
- The integration automatically refreshes tokens
- If issues persist, remove and re-add the integration

## API Rate Limits

- **Default**: 2500 requests per 5 minutes
- **Custom limits**: Contact Hinen technical support

## Development

### Prerequisites
- Home Assistant development environment
- Hinen developer account
- Python 3.11+

### Testing
```bash
# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install homeassistant

# Run Home Assistant in development mode
hass -c config
```

## Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/jnctech/hinen-solar-homeassistant/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/jnctech/hinen-solar-homeassistant/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/jnctech/hinen-solar-homeassistant/wiki)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- Thanks to Hinen/celinksmart for API access
- Home Assistant community for integration framework
- All contributors and testers

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by Hinen or celinksmart.
