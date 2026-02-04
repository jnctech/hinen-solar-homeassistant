# Why Mobile App Doesn't Conflict - Analysis

## Key Observation
The **Hinen Solar mobile app** works simultaneously with the **Hinen Power integration** using the same Hinen account, but **Hinen Solar Advanced integration** conflicts with Hinen Power.

This proves: **The Hinen API DOES support multiple concurrent sessions.**

---

## Hypothesis: Different API Endpoints or Methods

The mobile app likely uses **different API endpoints** or a **different authentication method** than the integrations.

### Possible Differences:

#### 1. **Mobile App Uses Different API**
- Mobile apps often use **different API versions** or **endpoints**
- Example: Mobile might use `/v2/` while integrations use `/open-api/`
- Mobile might use a different authentication scheme

#### 2. **Different OAuth Scopes**
- Mobile app might request different OAuth scopes
- Integration might request broader permissions
- Conflicting scopes could cause issues

#### 3. **Token Storage/Refresh Behavior**
- Mobile app might not refresh tokens as aggressively
- Integration might refresh more frequently, causing invalidation
- Timing of refresh could be critical

#### 4. **User Agent / Client Identification**
- Mobile app might send different headers
- API might treat "mobile" clients differently than "integration" clients
- Client type might affect session handling

---

## Investigation Needed

### Compare API Calls

**Mobile App API:**
- Capture mobile app traffic using proxy (mitmproxy, Charles)
- Identify API endpoints used
- Check authentication headers
- Compare with integration API calls

**Integration API:**
- Official Hinen Power: Uses `hinen_open.get_device_details()`
- Your integration: Uses `/iot-device/open-api/devices/info/{id}`

### Compare OAuth Flows

**Mobile App OAuth:**
- Likely uses standard OAuth2 mobile flow
- Might use different Client ID
- Might have different scope permissions

**Integration OAuth:**
- Uses authorization code flow
- Client ID: `3l5T3c2s` (yours), `6liMmES7` (official)
- Scope: Unknown (not explicitly set)

---

## Potential Root Causes

### Theory 1: API Endpoint Collision
**What if both integrations use the EXACT SAME endpoint at the SAME TIME?**

- Official Hinen Power calls `/iot-device/open-api/devices/info/{id}`
- Your integration calls `/iot-device/open-api/devices/info/{id}`
- Mobile app calls different endpoint: `/mobile/v2/device/{id}` (hypothetical)

**Result**: API might have endpoint-level locking or rate limiting

**Test**: Stagger update times between integrations (official: 60s, yours: 75s offset)

---

### Theory 2: WebSocket vs REST API
**Mobile app might use WebSockets for real-time updates**

- Mobile app connects once via WebSocket
- Integrations poll via REST API repeatedly
- Polling might conflict with WebSocket session

**Test**: Check if mobile app maintains persistent connection

---

### Theory 3: Token Type Difference
**Different token types for different clients**

- Mobile app: Refresh token never expires (or very long TTL)
- Integration: Refresh token expires after X hours
- Refreshing integration token invalidates other integration tokens (but not mobile tokens)

**Test**: Check token expiration times and refresh behavior

---

### Theory 4: Official Integration Bug
**The official integration might have a bug that YOUR integration triggers**

Observations:
- Official integration shows "Couldn't connect to Hinen"
- YOUR integration has no errors
- Mobile app has no errors

**Possible bug scenarios:**
1. Official integration doesn't handle multiple sessions gracefully
2. Official integration has hardcoded assumptions about being "only one"
3. Official integration's error handling is too aggressive

**Evidence needed:**
- Look at official integration's source code for session management
- Check if official integration caches anything globally
- See if official integration assumes exclusive device access

---

### Theory 5: Device Lock Mechanism
**Hinen API might lock devices during property updates**

- Reading device properties: No lock (multiple readers OK)
- Writing device properties: Lock required (exclusive access)

**Official Hinen Power includes WRITE operations** (control features):
- If official integration tries to WRITE
- And device is "locked" by another read
- Write might fail with "Couldn't connect"

**Your integration is READ-ONLY**, so it never locks the device.

**Mobile app might also be READ-ONLY** (just monitoring), so no conflict.

**Test**:
1. Disable all control features in official integration
2. See if conflict disappears

---

## Testing Plan

### Test 1: Standalone API Script
Run `test_api_standalone.py` while Hinen Power is running:
- If standalone script works → Confirms API supports multiple sessions
- If standalone script fails → Session limit confirmed

### Test 2: Staggered Updates
Modify your integration to update at offset times:
- Official: Updates at 0, 60, 120 seconds (minute boundaries)
- Yours: Updates at 15, 75, 135 seconds (offset by 15s)
- See if conflict reduces

### Test 3: Capture Mobile App Traffic
Use proxy to capture mobile app API calls:
```bash
# Install mitmproxy
pip install mitmproxy

# Run proxy
mitmproxy -p 8080

# Configure phone to use proxy
# Open Hinen Solar app
# Observe API calls in mitmproxy
```

### Test 4: Disable Official Integration's Write Operations
If official integration has config options:
- Disable all control features
- Make it read-only
- See if conflict disappears

### Test 5: Check Official Integration Source
Review official integration's coordinator:
```python
# Look for:
- Session management
- Token caching
- Device locking
- Exclusive access assumptions
```

---

## Recommended Next Steps

1. **Run standalone test script** (highest priority)
   - Edit credentials in `test_api_standalone.py`
   - Run while Hinen Power is active
   - Monitor for 5 minutes
   - Check if errors occur

2. **Review official integration source** (if standalone works)
   - Check for bugs in official's session handling
   - Look for assumptions about exclusive access
   - Find actual error source

3. **Capture mobile app traffic** (if time permits)
   - Identify exact API differences
   - Compare with integration API calls

4. **Test read-only theory** (if official has write features)
   - Temporarily disable control features
   - See if conflict disappears

---

## Expected Outcomes

**If standalone script works without errors:**
→ API supports multiple sessions
→ Conflict is caused by official integration bug or behavior
→ Solution: Fix official integration or work around it

**If standalone script shows errors:**
→ Session limit exists at API level
→ Mobile app uses different API/authentication
→ Solution: Use different Hinen account or choose one integration

---

**Status**: Investigation in progress
**Next**: Run standalone test script
