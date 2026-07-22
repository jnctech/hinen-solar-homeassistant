# Hinen Solar Advanced

Monitoring **and control** for Hinen solar inverters, PV, and battery storage via
the Hinen Open API. You supply your own developer Client ID/Secret — nothing is
shared or hard-coded.

- **67 sensors** — PV strings, external/AC-coupled PV (e.g. a Solis on the PV
  meter), grid, battery, temperatures, the full energy-flow matrix, daily &
  lifetime energy, solar yield, and battery health (SOH, cell voltages/temps).
- **7 controls** — work-mode selector + SOC-limit and charge/discharge-power
  setpoints, with **verified writes** so automations enforcing charging rules
  fail loudly instead of silently drifting.
- **No third-party Python dependency** — uses Home Assistant's Application
  Credentials + OAuth2 framework.

**Requirements:** HA 2024.12.0+ and your own credentials from the
[Hinen Developer Portal](https://developer.celinksmart.com/en_US/feedback).

Can run alongside the official `hinen_power` integration. For the Energy Dashboard,
use **Total Yield** as the Solar production source.

[Full documentation →](https://github.com/jnctech/hinen-solar-homeassistant)
