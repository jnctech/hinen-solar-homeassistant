# Final Conflict Analysis & Solution

## Summary of Findings

### Key Differences Between Integrations

#### Official Hinen Power Integration:
- Uses external library: `hinen-open-api==1.0.0`
- Authentication via `AsyncConfigEntryAuth` (Home Assistant application credentials)
- API calls abstracted through library methods like `hinen_open.get_device_details()`
- Updates every 1 minute via coordinator
- **Has control features** (write operations to devices)

#### Your Hinen Solar Advanced Integration:
- **Direct API calls** using aiohttp (no external library)
- Manual OAuth2 token management (get/refresh tokens directly)
- Direct HTTP requests to `/iot-device/open-api/devices/info/{id}`
- Updates every 60 seconds via coordinator
- **Read-only** (no write operations)

#### Mobile App (Working alongside Official):
- Different API endpoints likely (/mobile/v2/ vs /iot-device/)
- Possibly persistent WebSocket connection vs polling
- Different authentication flow (mobile OAuth)

---

## Root Cause Hypothesis

Based on the evidence, here are the most likely causes:

### Theory #1: Token/Session Management Difference ⭐ **MOST LIKELY**

**Official Integration:**
- Uses Home Assistant's `application_credentials` system
- Managed authentication through `AsyncConfigEntryAuth`
- Likely has session persistence and proper token refresh coordination

**Your Integration:**
- Manages tokens manually
- Refreshes tokens independently
- May be creating a NEW session that invalidates the official integration's session

**Evidence:**
- When you install yours, official shows "Couldn't connect to Hinen"
- When you remove yours, official works again
- Mobile app doesn't conflict (likely uses different auth method)

### Theory #2: API Endpoint Locking

The official integration uses `hinen-open-api` library which may:
- Maintain a persistent connection
- Have session pooling
- Your direct API calls might be disrupting this

---

## Why Mobile App Doesn't Conflict

Mobile apps typically:
1. Use **different API versions** (`/mobile/v2/` vs `/open-api/`)
2. Use **WebSocket** connections for real-time updates (not polling)
3. Have **mobile-specific OAuth scopes** that don't conflict with integration scopes
4. Use **refresh tokens with longer TTL** (mobile apps stay logged in for months)

Integrations:
1. Use **developer API** (`/iot-device/open-api/`)
2. **Poll via REST** every 60 seconds
3. Use **integration OAuth scopes** (potentially conflicting)
4. **Refresh tokens aggressively** (every update cycle checks expiration)

---

## The Solution

Based on the analysis, here's the recommended approach:

### Option 1: Use the Official Integration's Library (RECOMMENDED)

**Modify your integration to use `hinen-open-api` library** instead of direct API calls.

**Advantages:**
- Same authentication mechanism as official integration
- Proper session management
- May eliminate conflict
- Easier maintenance (library handles API changes)

**Disadvantages:**
- Dependency on external library
- Need to understand library API

**Implementation:**
1. Add `hinen-open-api==1.0.0` to manifest requirements
2. Replace your `api.py` with calls to the library
3. Use same `AsyncConfigEntryAuth` pattern as official integration

---

###Option 2: Different OAuth Application Type

**Request a different OAuth application type from Hinen** (if available).

**Ask Hinen if they have:**
- Separate OAuth scopes for "monitoring-only" vs "control" integrations
- Different client types (server vs integration)
- API keys instead of OAuth for read-only access

---

### Option 3: Coordinate Token Management

**Share authentication state** between integrations (complex but possible).

**Implementation:**
1. Check if official integration is installed
2. If yes, attempt to reuse its authentication
3. Subscribe to official integration's token refresh events
4. Don't create separate OAuth session

**Problem:** This creates tight coupling and is fragile.

---

### Option 4: Different API Endpoints

**Use mobile API endpoints** instead of integration endpoints (if accessible).

**Research needed:**
- Can integrations access `/mobile/v2/` endpoints?
- What authentication is required?
- Are the same device details available?

**If successful:**
- Would eliminate conflict (different API surface)
- Mobile app proves this API supports concurrent access

---

### Option 5: Document the Limitation

**Accept that both can't run together** and clearly document it.

**Implementation:**
1. Add conflict detection to config flow
2. Warn users during installation
3. Provide clear documentation
4. Suggest using separate Hinen accounts as workaround

**Config flow check:**
```python
async def async_step_user(self, user_input):
    # Check if official integration is installed
    for entry in self.hass.config_entries.async_entries():
        if entry.domain == "hinen_power":
            return self.async_abort(
                reason="conflict_detected",
                description_placeholders={
                    "message": "The official Hinen Power integration is already installed. "
                              "These integrations cannot run simultaneously. "
                              "Please use a separate Hinen account or choose one integration."
                }
            )
```

---

## Recommended Action Plan

### Phase 1: Immediate (Document Limitation)
1. ✅ Add conflict detection to config flow
2. ✅ Update README with warning
3. ✅ Document workaround (separate accounts)
4. ✅ Close Issue #2 with explanation

### Phase 2: Investigation (1-2 days)
1. ❓ Contact Hinen support about:
   - OAuth scope differences
   - Mobile API access for integrations
   - Best practices for multiple integrations
2. ❓ Research `hinen-open-api` library:
   - Check if it's open source
   - Understand its authentication flow
   - See if we can use it

### Phase 3: Implementation (if viable)
1. 🔧 Implement chosen solution (likely Option 1 or 5)
2. 🧪 Test thoroughly with both integrations
3. 📝 Update documentation
4. 🚀 Release RC3 or v1.0.0

---

## Current Recommendation

**For RC2/RC3:** Implement **Option 5** (document limitation) immediately:
- Add conflict detection
- Clear warning in docs
- Users can choose or use separate accounts

**For v1.0.0:** Attempt **Option 1** (use official library):
- If we can successfully use `hinen-open-api`
- And it eliminates the conflict
- Then both integrations can coexist

**If Option 1 fails:** Accept **Option 5** as permanent solution and clearly position integrations as alternatives, not complements.

---

## Testing Plan

To validate any solution:

1. **Install official Hinen Power**
   - Verify it works
   - Note which devices/entities appear

2. **Install modified integration**
   - Does conflict detection work?
   - If no detection, does official still work?
   - Do both update successfully?

3. **Monitor for 30 minutes**
   - Check for "Couldn't connect" errors
   - Verify both coordinators update
   - Check Home Assistant logs

4. **Reload integrations**
   - Reload official → yours still works?
   - Reload yours → official still works?

5. **Restart Home Assistant**
   - Both load successfully?
   - No startup errors?

---

**Status:** Analysis complete, awaiting decision on approach
**Priority:** High - blocks dual-integration use case
**Next Step:** Choose option and implement
