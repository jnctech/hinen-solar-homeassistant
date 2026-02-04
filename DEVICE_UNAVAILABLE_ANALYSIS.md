# Device Unavailable Issue Analysis

## Problem Statement
Official Hinen Power integration shows "Device Unavailable" when Hinen Solar Advanced (RC2) is installed, even though device identifier collision was fixed.

## Symptoms
- No 500 errors (fixed in RC2)
- Official integration shows "Device Unavailable"
- Both integrations are installed simultaneously
- Installation order doesn't matter

---

## Potential Root Causes

### 1. **API Session Limit** (Most Likely)
The Hinen API might enforce a **single active session per user account**.

**Theory**: When both integrations authenticate with the same Hinen account but different Client IDs, the API might:
- Invalidate older sessions when a new one is created
- Limit concurrent sessions per user account
- Rotate/expire tokens when multiple OAuth apps access the same account

**Evidence to Check**:
- Do both integrations use the same Hinen user account?
- Does the official integration work alone?
- Does our integration work alone?
- Do they fail only when both are running?

**Test**:
```
1. Install only official integration → Check if it works
2. Install only our integration → Check if it works
3. Install both → Check which one fails
4. Reload the failing one → Check if it temporarily works (displacing the other)
```

---

### 2. **Token Refresh Conflict**
Both integrations might be refreshing tokens simultaneously, causing race conditions.

**Our Integration**:
- Refreshes token when expiration is within 5 minutes
- Uses `async_refresh_access_token()` with refresh token

**Official Integration**:
- Uses `AsyncConfigEntryAuth` for token management
- Automatic token refresh via auth handler

**Conflict Scenario**:
1. Both integrations have tokens expiring soon
2. Both attempt to refresh simultaneously
3. Hinen API processes first refresh → invalidates refresh token
4. Second refresh fails → integration becomes unavailable

**Evidence to Check in Logs**:
- Token refresh timing between both integrations
- "Unauthorized" or "Invalid token" errors
- Which integration fails first

---

### 3. **API Rate Limiting**
Combined API calls from both integrations might exceed rate limits.

**Our Integration**:
- 2 API calls per 60s update cycle
- GET `/iot-device/open-api/devices`
- GET `/iot-device/open-api/devices/info/{device_id}`

**Official Integration**:
- Similar API call pattern
- Likely 2-3 calls per update

**Combined Load**:
- 4-5 API calls per minute per integration
- Total: ~8-10 calls/minute

**Default Hinen API Limit**:
- 2,500 requests per 5 minutes
- = 500 requests per minute

**Verdict**: Unlikely - we're well under the limit

---

### 4. **Shared Resource Lock**
The Hinen backend might lock device access when one integration is actively communicating.

**Theory**: Device properties endpoint might use pessimistic locking:
- Integration A fetches device info → locks device
- Integration B tries to fetch → gets "device unavailable"
- Integration A completes → unlocks device

**Evidence to Check**:
- Timing of API calls between integrations
- Whether failures are intermittent or permanent
- Error messages in API responses

---

### 5. **OAuth Scope Conflict**
Different Client IDs might request different OAuth scopes, causing conflicts.

**Our Integration**:
- Read-only access (no control features)
- Fetches device list and properties

**Official Integration**:
- Read + Write access (control features)
- Fetches device list, properties, and sets properties

**Theory**: The API might not allow simultaneous read-only and read-write sessions.

**Evidence to Check**:
- OAuth scopes granted to each Client ID
- Whether official integration uses write operations
- API error messages about permissions

---

## Diagnostic Steps

### Step 1: Check Logs
Look for these patterns in Home Assistant logs:

**For Official Integration** (`hinen_power`):
```
ERROR (MainThread) [custom_components.hinen_power.coordinator] Couldn't connect to Hinen
ERROR (MainThread) [custom_components.hinen_power.coordinator] UnauthorizedError
ERROR (MainThread) [custom_components.hinen_power] Error communicating with API
```

**For Our Integration** (`hinen`):
```
ERROR (MainThread) [custom_components.hinen.coordinator] Error communicating with API
ERROR (MainThread) [custom_components.hinen.api] Authentication failed
```

### Step 2: Check Token Refresh Timing
```
DEBUG (MainThread) [custom_components.hinen.api] Refreshing access token
DEBUG (MainThread) [custom_components.hinen_power] Token refresh
```

### Step 3: Check API Response Codes
Look for HTTP status codes in logs:
- `401 Unauthorized` → Token issue
- `403 Forbidden` → Permission issue
- `429 Too Many Requests` → Rate limiting
- `409 Conflict` → Resource conflict
- `503 Service Unavailable` → Backend issue

### Step 4: Test Isolation
**Test A**: Official integration only
```bash
# Remove our integration
# Restart HA
# Check if official works
```

**Test B**: Our integration only
```bash
# Remove official integration
# Restart HA
# Check if ours works
```

**Test C**: Both installed
```bash
# Install both
# Check which fails
# Reload the failing one
# Check if it displaces the other
```

---

## Possible Solutions

### Solution 1: Use Different Hinen Accounts
If the issue is session limits:
- Create a second Hinen account
- Add the same devices to both accounts
- Use Account A for official integration
- Use Account B for our integration

**Pros**: Completely isolates sessions
**Cons**: Requires multiple accounts, device sharing

---

### Solution 2: Stagger Update Intervals
Reduce simultaneous API calls:
- Official: Update every 60s (default)
- Ours: Update every 90s (configurable)

**Implementation**:
```python
# In options flow
vol.Optional("scan_interval", default=90): vol.All(
    vol.Coerce(int), vol.Range(min=60, max=300)
),
```

**Pros**: Simple, reduces API load
**Cons**: Doesn't fix root cause, less timely data

---

### Solution 3: Shared Session Manager
Create a shared authentication layer:
- Both integrations use the same access token
- Single token refresh mechanism
- Coordinate API calls

**Pros**: Eliminates session conflicts
**Cons**: Complex, requires major refactoring

---

### Solution 4: Detect Conflict and Warn User
Add conflict detection:
```python
# In config_flow.py
async def async_step_user(self, user_input):
    # Check if official integration is installed
    if "hinen_power" in self.hass.config_entries.async_domains():
        return self.async_abort(
            reason="official_integration_found",
            description_placeholders={
                "message": "The official Hinen Power integration is installed. "
                          "Running both integrations simultaneously may cause conflicts. "
                          "Consider using only one integration or separate Hinen accounts."
            }
        )
```

**Pros**: Prevents user frustration
**Cons**: Loses the benefit of running both

---

### Solution 5: API Call Coordination
Implement a shared coordinator that both integrations can use:
- Create a "meta" integration that manages Hinen API access
- Both integrations register as consumers
- Single set of API calls, data shared to both

**Pros**: Optimal API usage, no conflicts
**Cons**: Requires both integrations to adopt it

---

## Recommended Next Steps

1. **Collect Logs**:
   - Enable debug logging for both integrations
   - Reproduce the issue
   - Analyze error messages and timing

2. **Isolation Test**:
   - Test each integration independently
   - Confirm both work when alone
   - Confirm conflict when together

3. **Check Hinen API Documentation**:
   - Session limits
   - Concurrent access policies
   - OAuth scope interactions

4. **Contact Hinen Support**:
   - Ask about multiple Client IDs per account
   - Ask about session limits
   - Ask about best practices for multiple integrations

5. **Implement Temporary Workaround**:
   - Add warning in documentation
   - Suggest using separate accounts
   - Recommend choosing one integration

6. **Long-term Solution**:
   - Based on root cause analysis
   - Could be staggered intervals, shared session, or documented limitation

---

## Data Collection Commands

### Enable Debug Logging
Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.hinen: debug
    custom_components.hinen_power: debug
```

### Restart HA and Capture Logs
```bash
# Let both integrations run for 5 minutes
# Download logs: Settings → System → Logs → Download Full Log
```

### Filter Relevant Logs
```bash
grep -E "(hinen|hinen_power)" home-assistant.log > hinen_debug.log
```

---

**Status**: Investigation required
**Priority**: High - blocks users from running both integrations
**Next**: Collect logs and perform isolation testing
