"""OAuth2 authorization callback handler for Hinen Solar."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class HinenOAuth2CallbackView(HomeAssistantView):
    """Handle OAuth2 authorization callback."""

    requires_auth = False
    url = "/api/hinen_solar/oauth/callback"
    name = "api:hinen_solar:oauth:callback"

    async def get(self, request: web.Request) -> web.Response:
        """Handle GET request from OAuth provider."""
        hass: HomeAssistant = request.app["hass"]

        # Extract parameters from query string
        params = request.query

        _LOGGER.debug("OAuth callback received with params: %s", params)

        # Check for authorization code or error
        auth_code = params.get("code")
        error = params.get("error")
        state = params.get("state")

        if not state:
            return web.Response(
                text="Error: Missing state parameter",
                status=400,
            )

        # Build user input data
        user_input: dict[str, Any] = {}

        if error:
            user_input["error"] = error
            user_input["error_description"] = params.get("error_description", "Authorization failed")
        elif auth_code:
            user_input["authorization_code"] = auth_code
        else:
            user_input["error"] = "no_code"
            user_input["error_description"] = "No authorization code received"

        # Store the authorization data in hass.data for the config flow to retrieve
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}

        hass.data[DOMAIN]["oauth_callback"] = user_input

        # Return HTML that closes the window and notifies the user
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Hinen Solar Authorization</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }
        .container {
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 400px;
        }
        .success {
            color: #4caf50;
            font-size: 48px;
            margin-bottom: 20px;
        }
        .error {
            color: #f44336;
            font-size: 48px;
            margin-bottom: 20px;
        }
        h1 {
            margin: 0 0 10px 0;
            font-size: 24px;
        }
        p {
            color: #666;
            margin: 10px 0;
        }
        .close-msg {
            margin-top: 20px;
            font-size: 14px;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
"""

        if auth_code:
            html_content += f"""
        <div class="success">✓</div>
        <h1>Authorization Successful!</h1>
        <p>Submitting authorization code...</p>
        <p class="close-msg">This window will close automatically.</p>
        <input type="hidden" id="auth_code" value="{auth_code}">
"""
        else:
            error_msg = user_input.get("error_description", "Unknown error")
            html_content += f"""
        <div class="error">✗</div>
        <h1>Authorization Failed</h1>
        <p>{error_msg}</p>
        <p class="close-msg">Please return to Home Assistant and try again.</p>
"""

        html_content += """
    </div>
    <script>
"""

        if auth_code:
            html_content += f"""
        // Auto-fill and submit the authorization code in the opener window
        if (window.opener && !window.opener.closed) {{
            try {{
                // Find the authorization code input field in the config flow
                const authInput = window.opener.document.querySelector('input[name="authorization_code"]');
                if (authInput) {{
                    authInput.value = "{auth_code}";
                    authInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    authInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

                    // Find and click the submit button
                    const submitButton = window.opener.document.querySelector('button[type="submit"]');
                    if (submitButton) {{
                        setTimeout(function() {{
                            submitButton.click();
                            window.close();
                        }}, 500);
                    }} else {{
                        // If no submit button, just close after a delay
                        setTimeout(function() {{ window.close(); }}, 2000);
                    }}
                }} else {{
                    // Input not found, close after delay
                    setTimeout(function() {{ window.close(); }}, 3000);
                }}
            }} catch (e) {{
                console.error('Failed to auto-submit:', e);
                setTimeout(function() {{ window.close(); }}, 3000);
            }}
        }} else {{
            // No opener window, just close
            setTimeout(function() {{ window.close(); }}, 3000);
        }}
"""
        else:
            html_content += """
        // Keep window open on error so user can see the message
"""

        html_content += """
    </script>
</body>
</html>
"""

        return web.Response(
            text=html_content,
            content_type="text/html",
        )


@callback
def async_register_callback_view(hass: HomeAssistant) -> None:
    """Register the OAuth callback view."""
    hass.http.register_view(HinenOAuth2CallbackView())
    _LOGGER.debug("Registered OAuth callback view at %s", HinenOAuth2CallbackView.url)
