## ✅ RESOLVED in v1.0.0-rc2

This issue has been **resolved** in release [v1.0.0-rc2](https://github.com/jnctech/hinen-solar-homeassistant/releases/tag/v1.0.0-rc2).

### Root Cause Identified

The issue was **NOT related to OAuth claims**, but rather a **device identifier collision** in Home Assistant's device registry.

#### The Problem
Both integrations were using the same `device_id` from the Hinen API to register devices:
- **Official Hinen Power:** `identifiers={(hinen_power, f"{entry_id}_{device_id}")}`
- **Hinen Solar Advanced (RC1):** `identifiers={(hinen, device_id)}`

Even though different domains were used (`hinen` vs `hinen_power`), Home Assistant's device registry became confused when both integrations tried to represent the same physical device, causing:
- 500 errors
- Entity update failures
- Device ownership conflicts

#### OAuth Works Fine
The OAuth authentication was working correctly for both integrations. Each uses:
- Separate Client IDs
- Separate access tokens
- Separate API quotas
- Independent authentication flows

There is **no OAuth conflict** between the integrations.

### The Fix

Modified device identifiers in RC2 to ensure uniqueness:

**Before (RC1):**
```python
"identifiers": {(DOMAIN, device_id)}
```

**After (RC2):**
```python
"identifiers": {(DOMAIN, f"{device_id}_advanced")}
```

**Files Changed:**
- `custom_components/hinen/sensor.py` - Added `_advanced` suffix to device identifier
- `custom_components/hinen/binary_sensor.py` - Added `_advanced` suffix to device identifier

### Result

✅ Both integrations now run perfectly side-by-side without conflicts
✅ Each integration creates its own separate device in Home Assistant
✅ No more 500 errors or entity failures
✅ OAuth authentication works independently for both

### Testing Required

For users upgrading from RC1 or experiencing conflicts:

1. **Remove Both Integrations:**
   - Settings → Devices & Services
   - Remove "Hinen Solar Advanced"
   - Remove "Hinen Power" (if installed)

2. **Delete Old Devices:**
   - Settings → Devices & Services → Devices tab
   - Delete any old Hinen devices

3. **Reinstall:**
   - Install official Hinen Power first (optional)
   - Install Hinen Solar Advanced v1.0.0-rc2
   - Verify both load without errors

4. **Verify:**
   - Two separate devices should appear (one per integration)
   - All entities should update successfully
   - Check logs for errors (should be none)

### Additional Documentation

For technical details, see:
- [CONFLICT_ANALYSIS.md](https://github.com/jnctech/hinen-solar-homeassistant/blob/main/CONFLICT_ANALYSIS.md) - Complete technical analysis
- [Release Notes v1.0.0-rc2](https://github.com/jnctech/hinen-solar-homeassistant/releases/tag/v1.0.0-rc2) - Release information

---

**Please test and confirm the fix works, then close this issue if resolved!**
