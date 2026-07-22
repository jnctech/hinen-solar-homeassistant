# Changelog

## 1.0.1 — 2026-07-22

### Added
- **Self-hosted brand icon** (`brand/icon.png` + `icon@2x.png`) — the Hinen logo now
  shows in Home Assistant 2026.3+ via the local brands proxy (no CDN dependency).
- README **Troubleshooting** (OAuth redirect reachability) and **Removal** sections.

### Changed
- HACS validation now runs the full check set (the temporary `brands` ignore is gone).
- Test fixtures use synthetic device identifiers.

## 1.0.0 — 2026-07-22

A near-complete rewrite onto a robust, dependency-free architecture, validated
end-to-end against a live inverter.

### Authentication
- Rewritten to Home Assistant's **Application Credentials + OAuth2 framework**
  with a JWT-state callback, replacing the previous hand-rolled `window.opener`
  flow that never authenticated successfully.
- **No third-party Python dependency** — the token exchange/refresh and API client
  are self-contained.
- Region is detected from the OAuth callback (the manual region dropdown is gone).
- Reauthentication flow added.

### Sensors (34 → 67)
- **External/AC-coupled PV** (`PV Meter Power`) — e.g. a Solis metered by the Hinen
  inverter; `PV Generation Power` is the whole-array total.
- Full **power-flow matrix** (PV/grid/battery → load/grid/battery) and daily +
  lifetime energy for each flow.
- **Solar yield**: `Daily Yield` and `Total Yield` (the Energy-Dashboard
  "Solar production" source).
- **Battery health**: SOH, pack quantity, cell min/max voltage & temperature,
  ISO resistance, power factor.
- Fixed `Rated Power` to apparent power (VA) instead of W.

### Controls (new)
- **Work Mode** select and SOC-limit / charge-discharge-power number setpoints.
- **Verified writes**: set → refresh → read-back; raises if the inverter doesn't
  accept the change, so automations enforcing charging rules fail loudly instead
  of silently drifting. Controls display the commanded value immediately.

### Quality
- Real test suite (`hass` + `aioclient_mock`, no MagicMock): 20 tests, ~90%
  coverage. CI: ruff, pytest, hassfest, HACS validation.
- Minimum Home Assistant version: **2024.12.0**.
- Can run alongside the official `hinen_power` integration.
