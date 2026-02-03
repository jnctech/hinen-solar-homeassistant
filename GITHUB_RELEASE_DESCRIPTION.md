# 🚀 Hinen Solar Advanced v1.0.0-rc1

**First Release Candidate** - Advanced monitoring integration with 35+ sensors for Hinen solar systems.

## What's This?

**Hinen Solar Advanced** provides comprehensive monitoring for power users who want detailed insights beyond the basic sensors. Works alongside the [official Hinen Power integration](https://github.com/Hinen-IoT/ha_hinen_power) - run both together!

### Key Features

✅ **35+ Sensors** - 3x more than official integration
✅ **PV String Monitoring** - Track each of 4 solar panel strings individually
✅ **3-Phase Grid Monitoring** - Per-phase voltage, current, power, frequency
✅ **Battery Health** - Voltage, current, temperature, SOC
✅ **Energy Statistics** - Daily, monthly, yearly, lifetime totals
✅ **Energy Dashboard Ready** - Full HA Energy Dashboard support
✅ **Multi-Region** - EU, Asia-Pacific, Australia data centers

## Installation

### HACS (Recommended)
1. HACS → Integrations → ⋮ → Custom repositories
2. Add: `https://github.com/jnctech/hinen-solar-homeassistant`
3. Category: Integration
4. Search "Hinen Solar Advanced" → Download
5. Restart Home Assistant

### Prerequisites
- Hinen developer credentials (Client ID/Secret) from [Hinen Developer Platform](https://developer.celinksmart.com)
- Contact Hinen support for developer access
- Active Hinen account with registered devices

## Configuration
1. Add Integration → "Hinen Solar Advanced"
2. Enter Client ID, Client Secret, Region
3. Follow OAuth link → Authorize
4. Paste authorization code
5. Done! 35+ sensors appear automatically

## What's Included

**Power Sensors:** PV generation, battery, load, grid, system power
**Battery:** SOC, voltage, current, temperature, capacity
**PV Strings:** Voltage, current, power for 4 strings
**Grid:** 3-phase voltage, current, power, frequency
**Energy:** Daily/total consumption, generation, grid feed-in, purchases
**Binary:** Online status, battery charging state

## RC1 Notes

⚠️ **Release Candidate** - Early adopters welcome! Please report issues.

**Current Limitations:**
- Requires developer credentials (each user gets their own from Hinen)
- Read-only monitoring (no controls - use official integration for that)
- API efficient: 0.4% of rate limit per user at default settings

**Feedback Welcome:**
- 🐛 Report bugs: [Issues](https://github.com/jnctech/hinen-solar-homeassistant/issues)
- 💡 Feature ideas: [Discussions](https://github.com/jnctech/hinen-solar-homeassistant/discussions)

## Comparison

| Feature | Official Hinen Power | Hinen Solar Advanced (This) |
|---------|---------------------|----------------------------|
| Sensors | 12 basic | 35+ detailed |
| Control | ✅ Work modes, settings | ❌ Monitoring only |
| PV Strings | ❌ | ✅ Individual tracking |
| 3-Phase Grid | ❌ | ✅ Per-phase metrics |
| Battery Health | Basic | ✅ Voltage, current, temp |
| Setup | Simple | Requires dev credentials |

**Best Setup:** Install both for complete coverage!

## Documentation

📖 [Full Documentation](https://github.com/jnctech/hinen-solar-homeassistant)
📖 [Quick Start Guide](https://github.com/jnctech/hinen-solar-homeassistant/blob/main/QUICK_START.md)
🐛 [Report Issues](https://github.com/jnctech/hinen-solar-homeassistant/issues)

## Roadmap to v1.0.0

- Gather RC feedback
- Fix reported bugs
- Investigate simplified authentication
- Production release after testing period

---

**License:** Apache 2.0
**Disclaimer:** Unofficial integration, not affiliated with Hinen/celinksmart

**Installation:** Add custom HACS repository → Download → Configure
