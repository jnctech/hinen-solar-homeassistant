# Hinen Solar Integration - Quick Start Guide

## ⚠️ Current Status

**This integration is currently in beta and awaiting testing.**

**Known Issue:** The Australia (AU) region OAuth authorization page has a bug that prevents authentication. If you're in the AU region, please wait for Hinen to fix this issue before attempting installation. Singapore (SG) and United Kingdom (GB) regions should work correctly.

**See [Issue #1](https://github.com/jnctech/hinen-solar-homeassistant/issues) for updates.**

---

## Prerequisites

Before you begin, make sure you have:

1. ✅ **Home Assistant** installed and running (2023.1.0 or later)
2. ✅ **HACS** installed (for easy installation)
3. ✅ **Hinen Developer Account** with Client ID and Client Secret
4. ✅ **Hinen Solar System** registered in your account

## Step 1: Get Your API Credentials

1. Contact **Hinen technical support** to request developer platform access
2. Log in to [Hinen Developer Platform](https://developer.celinksmart.com)
3. Navigate to: **Backend Management** → **Application List**
4. Copy your **Client ID** (example: `W4lHyHTK`)
5. Copy your **Client Secret** (example: `006afd4248684bed...`)
6. Note your **Region Code** (e.g., `AU` for Australia, `GB` for UK, `DE` for Germany)

## Step 2: Install the Integration

### Option A: HACS Custom Repository

1. Open **HACS** in Home Assistant
2. Click on **Integrations**
3. Click the **⋮** (three dots) in the top right corner
4. Select **Custom repositories**
5. Add this URL: `https://github.com/jnctech/hinen-solar-homeassistant`
6. Select Category: **Integration**
7. Click **Add**
8. Click **✓** to close the custom repositories dialog
9. Search for **"Hinen Solar"** in HACS integrations list
10. Click on **Hinen Solar**
11. Click **Download**
12. **Restart Home Assistant**

### Option B: Manual Installation

1. Download the [latest release](https://github.com/jnctech/hinen-solar-homeassistant/releases)
2. Extract the ZIP file
3. Copy the `custom_components/hinen` folder to your Home Assistant `config/custom_components/` directory
   - If `custom_components` doesn't exist, create it in your config folder
4. **Restart Home Assistant**

**Note:** This integration is not yet available in the default HACS repository. Use the custom repository method above.

## Step 3: Configure the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for **"Hinen Solar"**
4. Click on **Hinen Solar**

### Configuration Screen 1: Credentials

Enter your credentials:
- **Client ID**: `W4lHyHTK` (your actual ID)
- **Client Secret**: `006afd4248684bed...` (your actual secret)
- **Region Code**: Select your country (e.g., `Australia`)

Click **SUBMIT**

### Configuration Screen 2: Authorization

1. The integration will display an **Authorization URL**
2. **Copy the URL** (it looks like: `https://global.knowledge.celinksmart.com/#/auth?language=en_US&key=...`)
3. **Open the URL in a new browser tab**
4. **Log in** with your Hinen account credentials (the same you use in the mobile app)
5. **Authorize** the application
6. You will receive an **Authorization Code** on screen
7. **Copy the authorization code**
8. **Return to Home Assistant**
9. **Paste the authorization code** into the field
10. Click **SUBMIT**

## Step 4: Verify Installation

1. Go to **Settings** → **Devices & Services**
2. You should see **Hinen Solar** with your region
3. Click on it to see your devices
4. Click on a device to see all sensors

### What You Should See

Each solar system device will have approximately **39 entities**:

#### Power Sensors (6)
- PV Generation Power
- Battery Power
- Load Power
- Grid Power
- Total System Power
- Total Active Power

#### PV String Sensors (12)
- PV1-4 Voltage
- PV1-4 Current
- PV1-4 Power

#### Battery Sensors (6)
- Battery SOC (State of Charge)
- Battery Voltage
- Battery Current
- Battery Temperature
- Battery Capacity
- Battery Power

#### Grid Sensors (4)
- Grid R-Phase Voltage
- Grid R-Phase Current
- Grid R-Phase Power
- Grid Frequency

#### Energy Statistics (10)
- Daily Consumption
- Total Consumption
- Daily Grid Feed-in
- Total Grid Feed-in
- Daily Energy Purchased
- Total Energy Purchased
- Daily Charging Energy
- Total Charging Energy
- Daily Discharging Energy
- Total Discharging Energy

#### Inverter Sensors (3)
- Inverter Temperature
- DC-DC Temperature
- Rated Power

#### Binary Sensors (2)
- Online Status
- Battery Charging

## Step 5: Set Up Energy Dashboard (Optional)

1. Go to **Settings** → **Dashboards** → **Energy**
2. Click **ADD CONSUMPTION** for each category:

### Solar Production
- Select: `sensor.{your_device}_pv_generation_power`

### Battery Storage
- Select: `sensor.{your_device}_battery_power`

### Grid Consumption
- Select: `sensor.{your_device}_daily_energy_purchased`

### Return to Grid
- Select: `sensor.{your_device}_daily_grid_feed_in`

3. Save and wait for data to accumulate

## Step 6: Create a Dashboard (Optional)

Add sensors to your dashboard:

```yaml
type: entities
title: Solar System
entities:
  - entity: sensor.{device}_pv_generation_power
    name: Solar Production
  - entity: sensor.{device}_battery_power
    name: Battery Power
  - entity: sensor.{device}_battery_soc
    name: Battery Level
  - entity: sensor.{device}_load_power
    name: House Load
  - entity: sensor.{device}_grid_power
    name: Grid Power
  - entity: binary_sensor.{device}_online_status
    name: System Online
```

## Troubleshooting

### "Authentication failed"
- ✅ Double-check your Client ID and Client Secret
- ✅ Make sure you copied the authorization code correctly (no extra spaces)
- ✅ Try logging out and back into the Hinen platform

### "No devices found"
- ✅ Open the Hinen mobile app and verify your devices appear there
- ✅ Contact Hinen support to ensure your developer account has device access
- ✅ Try a different region code if you're unsure of your data center

### Sensors show "Unavailable"
- ✅ Check your internet connection
- ✅ Verify the integration shows as "Connected" in Settings → Devices & Services
- ✅ Try reloading the integration
- ✅ Check Home Assistant logs: Settings → System → Logs

### Token expired
- The integration automatically refreshes tokens
- If you see persistent authentication errors:
  1. Go to Settings → Devices & Services
  2. Find Hinen Solar
  3. Click the three dots (⋮)
  4. Select "Delete"
  5. Re-add the integration

## Support

- **GitHub Issues**: [Report bugs](https://github.com/jnctech/hinen-solar-homeassistant/issues)
- **Hinen Support**: Contact Hinen technical support for API access issues or OAuth problems

## Next Steps

- ✅ Explore all sensors in Developer Tools → States
- ✅ Set up automations based on battery SOC or grid power
- ✅ Create custom energy dashboards
- ✅ Share your setup with the community!

---

**Congratulations!** 🎉 Your Hinen solar system is now integrated with Home Assistant!
