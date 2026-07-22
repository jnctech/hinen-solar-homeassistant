# Hinen Solar Advanced — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/v/release/jnctech/hinen-solar-homeassistant)](https://github.com/jnctech/hinen-solar-homeassistant/releases)
[![License](https://img.shields.io/github/license/jnctech/hinen-solar-homeassistant.svg)](LICENSE)

Monitoring **and control** for Hinen solar inverters, PV systems, and battery
storage, via the Hinen Open API (`celinksmart.com`). Cloud-polling; you bring your
own developer credentials, so nothing is hard-coded or shared.

- **67 sensors** — PV strings, external/AC-coupled PV (e.g. a Solis on the Hinen PV
  meter), grid, battery, temperatures, the full energy-flow matrix, daily/lifetime
  energy, solar **yield**, and battery health (SOH, cell voltages/temps).
- **7 controls** — work-mode selector plus SOC-limit and charge/discharge-power
  setpoints, with **verified writes** (a write that the inverter doesn't accept
  raises an error, so automations enforcing charging rules never silently drift).
- **No third-party Python dependency** — authentication uses Home Assistant's own
  Application Credentials + OAuth2 framework; the API client is self-contained.

## Requirements

- Home Assistant **2024.12.0** or newer.
- Your own **Client ID** and **Client Secret** from the
  [Hinen Developer Portal](https://developer.celinksmart.com/en_US/feedback).
- A Hinen account with at least one commissioned device.

## Installation (HACS)

1. HACS → **Integrations** → ⋮ → **Custom repositories**.
2. Add `https://github.com/jnctech/hinen-solar-homeassistant`, category **Integration**.
3. Install **Hinen Solar Advanced**, then restart Home Assistant.

## Setup

1. **Settings → Devices & Services → Add Integration → “Hinen Solar Advanced”.**
2. Enter:
   - **Authorization page language** (English or 简体中文),
   - **Client ID** and **Client Secret** (from the developer portal),
   - **Home Assistant address** — the base URL of your instance with **no trailing
     slash** (e.g. `http://homeassistant.local:8123`). It must be reachable from the
     browser you complete authorization in.
3. You’ll be sent to Hinen’s page — **choose your region and sign in**.
4. You’re redirected back; the integration verifies your devices and creates the
   entry. Your region is detected automatically (no dropdown to get wrong).

### Compatibility with the official integration

This integration **can run alongside** the official
[`hinen_power`](https://github.com/Hinen-IoT/ha_hinen_power) integration — it uses a
distinct domain, callback path, and device identifiers. API usage is small
(2 requests per device per poll), so running both stays well within rate limits.

## Entities

**Sensors** (per device): PV1/PV2 voltage·current·power, **PV Meter Power**
(external/AC-coupled PV such as a Solis), **PV Generation Power** (whole-array
total), grid voltage·current·power·frequency, battery power·voltage·current·
temperature·SOC, inverter/DC-DC temperatures, the power-flow matrix
(PV→battery/load/grid, grid→load/battery, battery→load/grid), daily & lifetime
energy for each flow, **Daily Yield** / **Total Yield**, and battery health
diagnostics (SOH, pack quantity, cell min/max voltage & temperature, ISO
resistance, power factor). Two binary sensors: online status, battery charging.

**Controls** (per device): **Work Mode** (Self-use / Battery priority / Feed-in /
Time of use / Power-saving) and setpoint numbers — Max Charge SOC, Forced Charge
Cutoff SOC, Min Discharge SOC, Forced Discharge Cutoff SOC, Charge/Discharge Power
Limit.

### Energy Dashboard

Use **Total Yield** (`CumulativeProductionActive`) as your **Solar production**
source — it is the whole-array lifetime yield (matches the Hinen app), unlike the
per-string sensors. Use **Total Grid Feed-in** for return-to-grid and **Total
Energy Purchased** for grid consumption.

## Reliability of controls

Every control write does **set → refresh → read-back**. If the inverter reports
neither the new value nor its commanded “shadow”, the write raises
`HomeAssistantError` — so an automation enforcing a charging rule sees the failure
instead of assuming success. Controls display the commanded value immediately while
the inverter’s reported value catches up on the next poll.

## Troubleshooting

- **Stuck on the Hinen login page, or "redirect URI mismatch".** The **Home
  Assistant address** you entered must be the exact base URL you reach HA on from
  the browser where you complete sign-in, with **no trailing slash** — and that
  same URL must be registered as an allowed redirect/callback for your Client ID in
  the developer portal. External access (e.g. Nabu Casa) works only if you sign in
  through that same external URL.
- **"invalid_grant" / authorization fails after redirect.** The one-time code
  expired or was reused — start **Add Integration** again and complete sign-in
  promptly.
- **No devices found after login.** The Hinen account must have at least one
  *commissioned* device; a registered-but-uncommissioned inverter returns none.
- **Token refresh errors in the log.** Re-run the integration's **Reconfigure** /
  reauthentication flow to mint a fresh token; check the developer-portal
  credentials are still active.

## Removal

1. **Settings → Devices & Services**, open **Hinen Solar Advanced**, use the ⋮ menu
   on the integration entry and choose **Delete**. This removes the config entry,
   its devices, and all entities.
2. *(Optional)* If you no longer use any integration that relies on them, remove the
   Hinen **Application Credentials**: **Settings → Devices & Services → ⋮
   (top-right) → Application Credentials**, then delete the Hinen entry.
3. *(Optional)* To uninstall the code: HACS → **Hinen Solar Advanced** → **Remove**,
   then restart Home Assistant.

Deleting the integration does **not** change any settings on the inverter itself.

## Development

```bash
pip install -r requirements_test.txt
pytest            # real tests: hass + aioclient_mock (no MagicMock)
ruff check custom_components/hinen tests
ruff format --check custom_components/hinen tests
```

CI runs ruff, pytest (with coverage), `hassfest`, and HACS validation.

## Credits

Not affiliated with or endorsed by Hinen. “Hinen” and related marks belong to their
owners. Built for the Home Assistant community.

## License

[Apache-2.0](LICENSE).
