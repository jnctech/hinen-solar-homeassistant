# Release v1.0.0-rc1 - Hinen Solar Advanced

**🚀 First Release Candidate** - Advanced monitoring integration for Hinen solar systems

---

## 🎯 What is Hinen Solar Advanced?

**Hinen Solar Advanced** is a comprehensive monitoring integration for Home Assistant that provides **35+ detailed sensors** for Hinen solar inverters, battery storage, and PV systems. This integration focuses on advanced monitoring and works alongside the [official Hinen Power integration](https://github.com/Hinen-IoT/ha_hinen_power).

### Why This Integration?

**Official Hinen Power Integration:**
- ✅ 12 basic sensors (power, SOC, energy totals)
- ✅ Control features (work modes, charge/discharge settings)
- ✅ Suitable for most users

**Hinen Solar Advanced (This Integration):**
- ✅ **35+ sensors** - 3x more monitoring data
- ✅ **PV String Monitoring** - Individual tracking of up to 4 solar panel strings
- ✅ **3-Phase Grid Monitoring** - Per-phase voltage, current, power, frequency
- ✅ **Battery Health Metrics** - Voltage, current, temperature, SOC
- ✅ **Detailed Energy Statistics** - Daily, monthly, yearly, and lifetime totals
- ✅ **Binary Sensors** - Online status, battery charging state
- ✅ **Energy Dashboard Ready** - Full compatibility with HA Energy Dashboard

**You can run both integrations together for complete coverage!**

---

## ✨ Features

### 📊 35+ Comprehensive Sensors

**Power Monitoring (6 sensors):**
- PV Generation Power
- Battery Power (charge/discharge)
- Load Power (consumption)
- Grid Power (import/export)
- Total System Power
- Inverter Output Power

**Battery Management (5 sensors):**
- State of Charge (SOC)
- Battery Voltage
- Battery Current
- Battery Temperature
- Battery Capacity

**PV String Monitoring (12 sensors - 4 strings × 3 metrics):**
- PV1-4 Voltage
- PV1-4 Current
- PV1-4 Power

**3-Phase Grid Monitoring (10 sensors):**
- R/S/T Phase Voltage
- R/S/T Phase Current
- R/S/T Phase Power
- Grid Frequency

**Energy Statistics (10+ sensors):**
- Daily/Total Consumption
- Daily/Total Generation
- Daily/Total Grid Feed-in
- Daily/Total Energy Purchased
- Daily/Total Battery Charging
- Daily/Total Battery Discharging
- Monthly/Yearly aggregates

**Binary Sensors (2):**
- Online Status
- Battery Charging State

### 🌍 Multi-Region Support

Supports all Hinen data centers:
- **Europe:** 30+ countries (GB, DE, FR, ES, IT, NL, BE, PL, SE, AT, CH, PT, IE, DK, FI, NO, GR, CZ, and more)
- **Asia-Pacific:** Singapore, Pakistan
- **Australia:** Australia, New Zealand

### 🔐 Secure OAuth2 Authentication

- Industry-standard OAuth2 authentication
- Automatic token refresh
- Secure credential storage
- No password storage required

### 🏠 Energy Dashboard Integration

All sensors properly configured for Home Assistant Energy Dashboard:
- Solar production tracking
- Battery charge/discharge cycles
- Grid import/export monitoring
- Home consumption analysis

---

## 📋 Prerequisites

### Required

1. **Hinen Developer Credentials:**
   - Contact Hinen technical support for developer platform access
   - Obtain Client ID and Client Secret from [Hinen Developer Platform](https://developer.celinksmart.com)
   - Navigate: Backend Management → Application List

2. **Hinen Account:**
   - Active account with registered solar devices
   - Accessible via Hinen mobile app

3. **Region Code:**
   - Know your region (e.g., AU, GB, DE, SG)
   - See [supported regions](https://github.com/jnctech/hinen-solar-homeassistant#supported-regions)

### System Requirements

- Home Assistant 2023.1.0 or later
- HACS (recommended for installation)
- Internet connectivity for cloud API access

---

## 🚀 Installation

### Via HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click **⋮** (three dots) → **Custom repositories**
4. Add: `https://github.com/jnctech/hinen-solar-homeassistant`
5. Category: **Integration**
6. Click **Add**
7. Search for **"Hinen Solar Advanced"**
8. Click **Download**
9. **Restart Home Assistant**

### Manual Installation

1. Download the [latest release](https://github.com/jnctech/hinen-solar-homeassistant/releases)
2. Extract to `config/custom_components/hinen/`
3. Restart Home Assistant

---

## ⚙️ Configuration

### Setup Steps

1. **Settings** → **Devices & Services** → **Add Integration**
2. Search for **"Hinen Solar Advanced"**
3. Enter your **Client ID** and **Client Secret**
4. Select your **Region**
5. Follow the OAuth authorization link
6. Sign in with your Hinen account
7. Copy and paste the authorization code
8. Done! 35+ sensors will appear automatically

### Configuration Options

- **Scan Interval:** 30-300 seconds (default: 60 seconds)
- Configurable via integration options

---

## 🔧 What's New in RC1

### Initial Release Features

✅ **Complete OAuth2 Implementation**
- Fixed redirectUrl parameter requirement
- Automatic token refresh
- Multi-region support

✅ **35+ Sensors Implemented**
- All power, battery, PV, grid sensors
- Energy statistics sensors
- Binary sensors

✅ **HACS Compatible**
- Custom repository support
- Proper manifest configuration
- Energy Dashboard integration

✅ **Comprehensive Documentation**
- README with full feature list
- Quick start guide
- Troubleshooting section

### Known Limitations (RC1)

⚠️ **User Credentials Required:**
- Each user must obtain their own Hinen developer credentials
- Contact Hinen support for developer platform access
- Future releases may provide simplified authentication

⚠️ **Read-Only Monitoring:**
- This integration provides monitoring only
- No control features (work modes, charge settings)
- Use official Hinen Power integration for controls

⚠️ **API Rate Limits:**
- Default: 2500 requests per 5 minutes per Client ID
- Single user impact: ~0.4% of limit (very safe)
- Each user manages their own quota

---

## 📊 API Usage

**Very Efficient:**
- 2 API calls per update cycle
- Default 60s interval: 10 calls per 5 minutes (0.4% of limit)
- Aggressive 30s interval: 20 calls per 5 minutes (0.8% of limit)
- No risk of hitting rate limits for normal usage

---

## 🐛 Known Issues

### OAuth Authorization
- AU region OAuth page previously had JavaScript errors (now fixed with redirectUrl parameter)
- Authorization codes expire in 5-10 minutes (get fresh code if expired)

### First-Time Setup
- Developer credentials must be obtained from Hinen support
- May take 1-2 business days for approval

---

## 🔄 Upgrade Path

**This is a new integration** - no upgrade from previous versions.

**Running Alongside Official Integration:**
- Both integrations can coexist safely
- Different domains: `hinen` vs `hinen_power`
- No conflicts expected

---

## 📝 Feedback & Support

This is a **Release Candidate** - your feedback is valuable!

**Report Issues:**
- 🐛 [GitHub Issues](https://github.com/jnctech/hinen-solar-homeassistant/issues)
- Include Home Assistant version, logs, and steps to reproduce

**Feature Requests:**
- 💡 [GitHub Discussions](https://github.com/jnctech/hinen-solar-homeassistant/discussions)

**Documentation:**
- 📖 [Full README](https://github.com/jnctech/hinen-solar-homeassistant)
- 📖 [Quick Start Guide](https://github.com/jnctech/hinen-solar-homeassistant/blob/main/QUICK_START.md)

---

## 🎯 Roadmap to v1.0.0

**Before Production Release:**
- [ ] Gather RC1 user feedback
- [ ] Fix any reported bugs
- [ ] Investigate simplified authentication options
- [ ] Contact Hinen for custom API limit quotation
- [ ] Consider shared credentials model (if economical)

**Target:** v1.0.0 production release after successful RC testing period

---

## 👏 Acknowledgments

- Thanks to Hinen/celinksmart for API access
- Home Assistant community for integration framework
- Early adopters and testers

---

## ⚖️ License

Apache License 2.0 - See [LICENSE](LICENSE) file for details

---

## ⚠️ Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by Hinen or celinksmart. Use at your own risk. Always verify sensor data against your Hinen mobile app.

---

## 🔗 Links

- **Repository:** https://github.com/jnctech/hinen-solar-homeassistant
- **Issues:** https://github.com/jnctech/hinen-solar-homeassistant/issues
- **Official Hinen Power:** https://github.com/Hinen-IoT/ha_hinen_power
- **Hinen Developer Platform:** https://developer.celinksmart.com

---

**Installation Command (HACS):**
```
https://github.com/jnctech/hinen-solar-homeassistant
```

**Release Date:** February 3, 2026
**Version:** 1.0.0-rc1
**Status:** Release Candidate - Early Adopters Welcome!
