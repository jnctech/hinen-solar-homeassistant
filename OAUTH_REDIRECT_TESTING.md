# OAuth Redirect Testing Guide

## Branch: `oauth-redirect-handler`
## Version: `1.0.0-rc3-oauth-redirect`

This testing branch implements **automatic OAuth redirect handling** similar to the official Hinen Power integration, eliminating the need for users to manually copy/paste authorization codes.

---

## 🎯 What's New

### Automatic OAuth Flow
Instead of the manual process:
1. Click link → 2. Authorize → 3. Copy code → 4. Paste code

Users now get:
1. Click link → 2. Authorize → 3. **Done!** (automatic redirect)

### Key Features

✨ **HTTP Callback Endpoint**: `/api/hinen_solar/oauth/callback`
✨ **Auto-Detection**: Automatically detects Home Assistant URL
✨ **Configurable**: Users can customize redirect URL if needed
✨ **User-Friendly**: Beautiful success/failure pages
✨ **Fallback**: Manual code entry still available if automatic fails

---

## 📁 New Files

### 1. `auth_callback.py`
**Purpose**: HTTP endpoint that receives OAuth callbacks from Hinen

**Class**: `HinenOAuth2CallbackView`
**URL**: `/api/hinen_solar/oauth/callback`
**Method**: GET

**Flow**:
1. Hinen redirects user to this endpoint after authorization
2. Endpoint captures `code` parameter
3. Stores code in `hass.data[DOMAIN]["oauth_callback"]`
4. Displays success/failure page to user
5. Auto-closes window after 3 seconds (on success)

**HTML Response**:
- Success: Green checkmark, "Authorization Successful!"
- Failure: Red X, error description
- Auto-close script for seamless UX

---

## 🔧 Modified Files

### 1. `config_flow.py`

**New Imports**:
```python
from homeassistant.helpers.network import get_url
from .auth_callback import async_register_callback_view
```

**New Instance Variable**:
```python
self._redirect_url: str | None = None
```

**Changes in `async_step_user`**:

**Line 66**: Register callback view
```python
async_register_callback_view(self.hass)
```

**Line 72**: Capture redirect URL from user input
```python
self._redirect_url = user_input.get("redirect_url")
```

**Lines 75-82**: Auto-detect redirect URL if not provided
```python
if not self._redirect_url:
    try:
        base_url = get_url(self.hass, allow_internal=False, allow_ip=True)
        self._redirect_url = f"{base_url}/api/hinen_solar/oauth/callback"
    except Exception:
        self._redirect_url = "http://homeassistant.local:8123/api/hinen_solar/oauth/callback"
```

**Line 85**: Use redirect URL in OAuth authorization URL
```python
auth_url = f"{OAUTH_AUTHORIZE_URL}?language=en_US&key={self._client_id}&state=homeassistant&redirectUrl={self._redirect_url}"
```

**Lines 97-119**: Auto-detect default redirect for form default value
```python
default_redirect = "http://homeassistant.local:8123/api/hinen_solar/oauth/callback"
try:
    base_url = get_url(self.hass, allow_internal=False, allow_ip=True)
    default_redirect = f"{base_url}/api/hinen_solar/oauth/callback"
except Exception:
    pass
```

**Lines 125-127**: Add redirect_url to form schema
```python
vol.Optional("redirect_url", default=default_redirect): str,
```

**Changes in `async_step_authorize`**:

**Lines 139-151**: Check for automatic callback data
```python
# Check if we received the callback automatically
if DOMAIN in self.hass.data and "oauth_callback" in self.hass.data[DOMAIN]:
    callback_data = self.hass.data[DOMAIN].pop("oauth_callback")

    if "error" in callback_data:
        errors["base"] = "auth_failed"
        _LOGGER.error(...)
    else:
        user_input = {"authorization_code": callback_data["authorization_code"]}
```

**Line 193**: Store redirect_url in config entry
```python
"redirect_url": self._redirect_url,
```

### 2. `strings.json`

**User Step Description** (updated):
```json
"description": "Enter your Hinen Developer Platform credentials. You can obtain your Client ID and Client Secret from the Hinen Developer Platform at https://developer.celinksmart.com\n\nThe redirect URL will be auto-detected, but you can customize it if needed (e.g., for external access)."
```

**New Data Field**:
```json
"redirect_url": "OAuth Redirect URL (optional)"
```

**Authorize Step Description** (updated):
```json
"description": "Click the link below to authorize Home Assistant:\n\n{auth_url}\n\nAfter authorizing, you will be redirected back automatically. If automatic redirect fails, you can manually enter the authorization code below.\n\nRedirect URL: {redirect_url}"
```

**Data Field** (updated):
```json
"authorization_code": "Authorization Code (if needed)"
```

### 3. `manifest.json`

**Version** (updated for testing):
```json
"version": "1.0.0-rc3-oauth-redirect"
```

---

## 🧪 Testing Scenarios

### Scenario 1: Default Automatic Flow (Local Access)
**Setup**: Home Assistant accessed via `http://homeassistant.local:8123`

**Steps**:
1. Add integration → Enter credentials
2. Leave redirect URL as default (auto-detected)
3. Click authorization link
4. Authorize in Hinen portal
5. **Expected**: Automatic redirect → success page → auto-close → integration configured

**Verify**:
- No manual code entry required
- Success page displays
- Window closes automatically
- Integration completes setup

---

### Scenario 2: Custom Local URL
**Setup**: Home Assistant accessed via `http://192.168.1.100:8123`

**Steps**:
1. Add integration → Enter credentials
2. Redirect URL should auto-detect as `http://192.168.1.100:8123/api/hinen_solar/oauth/callback`
3. Click authorization link
4. Authorize in Hinen portal
5. **Expected**: Automatic redirect works

**Verify**:
- Auto-detection uses IP address
- Callback works with IP-based URL

---

### Scenario 3: Nabu Casa Remote Access
**Setup**: Home Assistant accessed via `https://xxxxxxxxxxxx.ui.nabu.casa`

**Steps**:
1. Add integration → Enter credentials
2. Redirect URL should auto-detect as `https://xxxxxxxxxxxx.ui.nabu.casa/api/hinen_solar/oauth/callback`
3. Click authorization link
4. Authorize in Hinen portal
5. **Expected**: Automatic redirect works with HTTPS

**Verify**:
- Auto-detection uses Nabu Casa URL
- HTTPS redirect works
- SSL/TLS handled properly

---

### Scenario 4: Custom External URL
**Setup**: Home Assistant accessed via custom domain `https://ha.example.com`

**Steps**:
1. Add integration → Enter credentials
2. Manually set redirect URL to `https://ha.example.com/api/hinen_solar/oauth/callback`
3. Click authorization link
4. Authorize in Hinen portal
5. **Expected**: Automatic redirect works

**Verify**:
- Custom URL works
- External domain accessible from Hinen OAuth

---

### Scenario 5: Manual Fallback
**Setup**: Automatic redirect fails for some reason

**Steps**:
1. Add integration → Enter credentials
2. Click authorization link
3. Authorize in Hinen portal
4. If redirect fails, copy code from URL
5. Manually paste code in "Authorization Code (if needed)" field
6. **Expected**: Manual entry still works

**Verify**:
- Authorization code field is optional (not required)
- Manual entry completes setup
- Both automatic and manual methods work

---

### Scenario 6: Authorization Failure
**Setup**: User denies authorization

**Steps**:
1. Add integration → Enter credentials
2. Click authorization link
3. **Deny** authorization in Hinen portal
4. **Expected**: Error page displays with reason

**Verify**:
- Error page shows failure message
- User returned to config flow with error
- Can retry authorization

---

## 🔍 Technical Verification

### Check Callback Registration
**Home Assistant Logs:**
```
DEBUG (MainThread) [custom_components.hinen.auth_callback] Registered OAuth callback view at /api/hinen_solar/oauth/callback
```

### Check Callback Received
**When OAuth redirects:**
```
DEBUG (MainThread) [custom_components.hinen.auth_callback] OAuth callback received with params: <QueryParams>
```

### Check Automatic Processing
**When config flow processes callback:**
```
INFO (MainThread) [homeassistant.components.config_entries] Successfully configured hinen
```

### HTTP Endpoint Verification
Test the callback endpoint directly:
```bash
curl "http://homeassistant.local:8123/api/hinen_solar/oauth/callback?code=test123&state=homeassistant"
```

**Expected**: HTML success page returned

---

## 🐛 Known Limitations

1. **Network Access**: Redirect URL must be accessible from user's browser
2. **Firewall**: Port 8123 must be accessible if using local network
3. **DNS**: `homeassistant.local` must resolve (or use IP/custom domain)
4. **Pop-up Blockers**: Some browsers may block the authorization window
5. **Session Persistence**: Flow state must persist during redirect

---

## 🔄 Comparison with Official Integration

### Official Hinen Power Integration
- Uses JWT-based state parameter
- Custom callback at `/auth/hinen/callback`
- Decodes state to resume flow
- Similar HTML response pages

### Our Implementation
- Simpler state parameter (`state=homeassistant`)
- Custom callback at `/api/hinen_solar/oauth/callback`
- Uses `hass.data` to pass data to flow
- Similar user experience

**Key Difference**: We store callback data in `hass.data` rather than encoding in JWT. This is simpler but requires the config flow to check for callback data.

---

## 📋 Testing Checklist

- [ ] Automatic redirect works with homeassistant.local
- [ ] Automatic redirect works with IP address
- [ ] Automatic redirect works with Nabu Casa URL
- [ ] Automatic redirect works with custom domain
- [ ] Manual code entry still works as fallback
- [ ] Error handling displays properly on authorization failure
- [ ] Success page displays and auto-closes
- [ ] Callback endpoint returns proper HTML
- [ ] Multiple concurrent setups don't interfere
- [ ] Logs show proper debug information
- [ ] Integration completes setup successfully
- [ ] Devices and entities appear correctly

---

## 🚀 Next Steps After Testing

If testing is successful:

1. **Merge to main branch**
   - Create PR from `oauth-redirect-handler` to `main`
   - Include test results in PR description

2. **Update version**
   - Change from `1.0.0-rc3-oauth-redirect` to `1.0.0-rc3`
   - Update release notes

3. **Documentation**
   - Update README with new OAuth flow description
   - Add screenshots of new authorization flow
   - Update QUICK_START guide

4. **Release**
   - Create GitHub release for RC3
   - Provide upgrade instructions
   - Highlight automatic redirect feature

5. **Community Feedback**
   - Monitor for issues
   - Gather user feedback
   - Address any bugs

6. **Stable Release**
   - After successful RC3 testing → v1.0.0
   - Submit to HACS default store

---

## 📞 Support

If you encounter issues during testing:

1. **Check Logs**: Settings → System → Logs → Filter by "hinen"
2. **Verify Network**: Ensure redirect URL is accessible
3. **Test Callback**: Use curl to test the endpoint directly
4. **Fallback**: Use manual code entry if automatic fails
5. **Report**: Create issue with logs and detailed steps

---

**Branch**: `oauth-redirect-handler`
**Created**: 2026-02-04
**Status**: Ready for testing
**Next**: Test all scenarios → Merge if successful
