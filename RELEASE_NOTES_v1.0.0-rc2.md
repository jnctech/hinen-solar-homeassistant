# 🔧 Hinen Solar Advanced v1.0.0-rc2 - Critical Compatibility Fix

## 🚨 CRITICAL FIX: Integration Compatibility

This release resolves a **critical device identifier collision** with the official Hinen Power integration that prevented both integrations from running simultaneously.

### What Was Fixed

**The Problem:**
- Both Hinen Solar Advanced and official Hinen Power integration were using the same `device_id` from the Hinen API
- This caused Home Assistant's device registry to become confused about which integration owned which device
- Result: 500 errors, entity update failures, and broken functionality when both were installed

**The Solution:**
- Modified device identifiers to include `_advanced` suffix
- Changed from: `identifiers={(DOMAIN, device_id)}`
- Changed to: `identifiers={(DOMAIN, f"{device_id}_advanced")}`

**The Result:**
- ✅ Both integrations now run perfectly side-by-side
- ✅ No more device registry conflicts
- ✅ No more 500 errors or entity failures
- ✅ Each integration maintains its own separate device entry

---

## 🎯 Why This Matters

Users can now enjoy the **best of both worlds**:

**Hinen Solar Advanced (this integration):**
- 35+ sensors for comprehensive monitoring
- PV string-level data (4 strings)
- 3-phase grid monitoring
- Detailed battery health metrics
- Advanced energy statistics

**Official Hinen Power:**
- 12 basic sensors
- Control features (work modes, battery settings)
- Simpler setup process

---

## 📦 Installation Notes

### For New Users
Simply install Hinen Solar Advanced v1.0.0-rc2 and it will work correctly whether or not you have the official integration installed.

### For Existing Users (Upgrading from RC1)

**IMPORTANT:** If you previously installed RC1, you must perform a clean installation:

1. **Remove Both Integrations:**
   - Go to Settings → Devices & Services
   - Remove "Hinen Solar Advanced" integration
   - Remove "Hinen Power" integration (if installed)

2. **Delete Old Devices:**
   - Go to Settings → Devices & Services → Devices tab
   - Find any Hinen devices and delete them manually

3. **Reinstall:**
   - Install official Hinen Power first (if desired)
   - Then install Hinen Solar Advanced v1.0.0-rc2
   - Both should load without errors

4. **Verify:**
   - You should see **two separate devices** in Home Assistant (one per integration)
   - All entities from both integrations should update successfully
   - Check logs for any errors (there should be none)

---

## 🔍 Technical Details

### Files Changed
- `custom_components/hinen/sensor.py` - Updated device identifier with `_advanced` suffix
- `custom_components/hinen/binary_sensor.py` - Updated device identifier with `_advanced` suffix
- `custom_components/hinen/manifest.json` - Version bump to 1.0.0-rc2
- `README.md` - Updated with RC2 notice and fix description
- `info.md` - Updated to RC2 with compatibility notice
- `CONFLICT_ANALYSIS.md` - New detailed technical analysis document

### Device Identifier Comparison

**Before (RC1):**
```python
"identifiers": {(DOMAIN, "abc123xyz")}  # Conflicts with official!
```

**After (RC2):**
```python
"identifiers": {(DOMAIN, "abc123xyz_advanced")}  # Unique!
```

**Official Hinen Power:**
```python
identifiers={(DOMAIN, f"{entry_id}_{device_id}")}  # Different pattern
```

---

## ✨ What's Included (Same as RC1)

### 📊 Comprehensive Monitoring
- **35+ sensors** for complete solar system visibility
- **PV String Monitoring** - Track up to 4 solar panel strings individually
- **3-Phase Grid Monitoring** - Essential for commercial installations
- **Battery Health Tracking** - Voltage, current, temperature, and SOC
- **Detailed Energy Statistics** - Daily, monthly, yearly breakdowns

### 🔌 Energy Dashboard Compatible
All sensors integrate seamlessly with Home Assistant's Energy Dashboard:
- Solar production tracking
- Battery charge/discharge monitoring
- Grid import/export metering
- Home consumption analysis

### 🔐 Secure Authentication
- OAuth2 authentication with automatic token refresh
- Multi-region support (Europe, Asia-Pacific, Australia)
- User-provided developer credentials for isolated API quotas

---

## 📋 Requirements

1. Hinen solar inverter or battery system
2. Developer credentials from [Hinen Developer Platform](https://developer.celinksmart.com)
3. Home Assistant Core 2023.1 or later

---

## 🚀 Installation

### Via HACS (Recommended)
1. Add custom repository: `https://github.com/jnctech/hinen-solar-homeassistant`
2. Search for "Hinen Solar Advanced" in HACS
3. Click Install
4. Restart Home Assistant

### Manual Installation
1. Download `hinen-solar-advanced-v1.0.0-rc2.zip`
2. Extract to `config/custom_components/hinen/`
3. Restart Home Assistant

---

## 📖 Setup Guide

1. Go to Settings → Devices & Services → Add Integration
2. Search for "Hinen Solar Advanced"
3. Enter your Client ID and Client Secret from Hinen Developer Platform
4. Select your region code (e.g., AU, GB, DE)
5. Click the authorization URL to approve access
6. Copy and paste the authorization code
7. Done! Your devices will appear automatically

---

## 🐛 Changelog

### v1.0.0-rc2 (2026-02-04)
- **CRITICAL FIX:** Device identifier collision with official Hinen Power integration
- Added `_advanced` suffix to device identifiers for uniqueness
- Updated documentation with compatibility information
- Added `CONFLICT_ANALYSIS.md` technical documentation

### v1.0.0-rc1 (2026-02-03)
- Initial release candidate
- 35+ sensors for comprehensive monitoring
- OAuth2 authentication
- Multi-region support
- Energy Dashboard integration

---

## 📚 Documentation

- [Full Documentation](https://github.com/jnctech/hinen-solar-homeassistant)
- [Quick Start Guide](https://github.com/jnctech/hinen-solar-homeassistant/blob/main/QUICK_START.md)
- [Conflict Analysis](https://github.com/jnctech/hinen-solar-homeassistant/blob/main/CONFLICT_ANALYSIS.md)
- [Issue Tracker](https://github.com/jnctech/hinen-solar-homeassistant/issues)

---

## 🙏 Credits

Built with ❤️ for the Home Assistant community. Special thanks to:
- Hinen for their developer API
- Early RC1 testers who helped identify the compatibility issue
- The Home Assistant community for feedback and support

---

## ⚠️ Known Issues

None at this time. Please report any issues on the [GitHub issue tracker](https://github.com/jnctech/hinen-solar-homeassistant/issues).

---

**License:** Apache 2.0
**Domain:** `hinen`
**Compatibility:** Home Assistant Core 2023.1+
**Status:** Release Candidate (testing phase)
