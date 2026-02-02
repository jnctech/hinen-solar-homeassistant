# Email to Hinen Support - Draft

---

**To:** Hinen Technical Support
**Subject:** URGENT - Australia OAuth Authorization Page Critical Bug (Client ID: 3l5T3c2s)

---

Hello Hinen Support Team,

I am contacting you regarding a critical bug in the Australia (AU) data center OAuth authorization page that is preventing me from integrating my Hinen solar system with Home Assistant.

## Issue Summary

When attempting to authorize my Home Assistant integration using OAuth2, the Australia data center authorization page displays a JavaScript error that prevents login.

## Account Information

- **Client ID:** 3l5T3c2s
- **Hinen User Account:** jc@jasoncole.info
- **Region:** Australia (AU)
- **Data Center:** https://au.iot-api.celinksmart.com
- **Developer Portal Account:** jc@jasonncole.com

## Error Details

**OAuth Authorization URL:**
```
https://global.knowledge.celinksmart.com/#/auth?language=en_US&key=3l5T3c2s&state=test_AU
```

**Error Message:**
```
TypeError: Failed to construct 'URL': Invalid URL
```

**When Error Occurs:**
The error appears when clicking the "Sign In" button on the authorization page.

**Browser Tested:**
[Please add your browser name and version, e.g., Chrome 131, Firefox 133, Edge 131, etc.]

## Verification Performed

To confirm this is an AU-specific issue, I tested the OAuth page with multiple regions:

| Region | Result | Notes |
|--------|--------|-------|
| AU (Australia) | ❌ JavaScript Error | "TypeError: Failed to construct 'URL': Invalid URL" |
| SG (Singapore) | ✅ Page Works | Shows "Your account does not exist" (correct, I'm in AU) |
| GB (United Kingdom) | ✅ Page Works | Shows "Your account does not exist" (correct, I'm in AU) |

This confirms:
1. My account correctly exists in the AU data center
2. The OAuth page works properly in other regions (SG, GB)
3. **Only the AU data center authorization page has this JavaScript bug**

I also verified that the AU API endpoints are functioning correctly:
- Token endpoint responds properly: ✅
- Device API is accessible: ✅
- AU region is recognized by the system: ✅

**This is specifically a bug in the AU OAuth web interface.**

## Impact

This bug affects all AU users attempting to use OAuth-based integrations with the Hinen Developer Platform API. It completely blocks:
- Third-party application integration
- Home Assistant integration
- Any OAuth2 authorization flow for AU accounts

## Technical Details for Your Development Team

The JavaScript error suggests an issue with URL construction in the authorization page code, likely:
- Missing or malformed URL parameter
- Incorrect string concatenation when building a URL
- Missing protocol (http://, https://) in a URL string
- A typo or undefined variable in the JavaScript code

The error occurs on the client side (browser), not the server side, indicating a front-end JavaScript issue.

## Urgency

This is blocking my Home Assistant integration development and testing. I have completed all integration code and am ready to deploy, but cannot proceed without a working OAuth authorization flow.

## Requested Resolution

Please choose one of the following solutions:

### Option 1: Fix the AU OAuth Page (Preferred)
Fix the JavaScript error on the Australia data center OAuth authorization page so the standard OAuth2 flow works correctly.

### Option 2: Temporary Authorization Code
Provide a manually-generated authorization code for my Client ID (3l5T3c2s) and account (jc@jasoncole.info) so I can test the integration while you fix the OAuth page.

### Option 3: Enable Signature Authentication
Enable signature-based authorization (Platform Development method) for my Client ID as a workaround:
- Client ID: 3l5T3c2s
- Request: Enable signature-based authentication

## Integration Details

I am developing a Home Assistant custom integration for Hinen solar systems that will allow thousands of Home Assistant users to monitor their Hinen solar, battery, and inverter systems. The integration is complete and production-ready, pending resolution of this OAuth issue.

## Follow-up

Please let me know:
1. When this issue will be escalated to your AU data center web development team
2. Expected timeline for resolution
3. If you need any additional information from me
4. If you can provide any of the workaround options listed above

I am available to provide additional testing, screenshots, browser console logs, or any other information that would help your team resolve this issue quickly.

Thank you for your urgent attention to this matter. I look forward to hearing from you soon.

Best regards,
[Your Name]

---

## Attachments to Include (Optional)

If Hinen requests more details, you can provide:

1. **Browser Console Log** - Screenshot or text of the JavaScript error
2. **Network Tab** - Screenshot showing the failed request
3. **Comparison Screenshots** - Working SG/GB login page vs broken AU page
4. **Test Results** - The detailed troubleshooting document showing API endpoint verification

---

## Follow-up Email Template (If No Response in 48 Hours)

**Subject:** FOLLOW-UP: AU OAuth Page Bug - Client ID 3l5T3c2s

Hello,

I am following up on my email from [DATE] regarding the critical OAuth authorization bug in the Australia data center.

This issue is still preventing all OAuth-based integrations for AU users. Has this been escalated to your development team?

If fixing the OAuth page will take time, could you please provide one of the workaround options I mentioned:
- A temporary authorization code for testing
- Enable signature-based authentication for my Client ID

Please provide an update on the status and expected resolution timeline.

Thank you,
[Your Name]

---

## Tips for Sending

1. **Send from your Hinen account email:** jc@jasoncole.info (or whatever email you use with Hinen)
2. **Mark as high priority** if your email client supports it
3. **Include browser details** - Add your specific browser name and version
4. **Be polite but firm** - Emphasize the urgency and impact
5. **Request escalation** - Ask them to escalate to their AU data center team
6. **Ask for timeline** - Request an ETA for resolution

## Expected Responses

**Best case:** They acknowledge the bug and provide a timeline or workaround
**Good case:** They request more information (be ready to provide screenshots)
**Okay case:** They escalate to technical team
**Bad case:** Generic response without acknowledgment - send follow-up

If you don't hear back within 2-3 business days, send the follow-up email above.
