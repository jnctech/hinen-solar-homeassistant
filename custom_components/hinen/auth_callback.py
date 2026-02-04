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
            html_content += """
        <div class="success">✓</div>
        <h1>Authorization Successful!</h1>
        <p>You can close this window and return to Home Assistant.</p>
        <p class="close-msg">This window will close automatically in 3 seconds...</p>
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
        // Auto-close window after 3 seconds if authorization was successful
"""

        if auth_code:
            html_content += """
        setTimeout(function() {
            window.close();
        }, 3000);
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
