"""Constants for the Hinen Solar integration."""

import logging

DOMAIN = "hinen"
MANUFACTURER = "Hinen"

LOGGER = logging.getLogger(__package__)

# OAuth2 endpoints (verified against Hinen's own integration + developer portal).
OAUTH_AUTHORIZE_URL = "https://global.knowledge.celinksmart.com/#/auth"
OAUTH_TOKEN_URL = "https://global.iot-api.celinksmart.com/iot-global/open-platforms/auth/token"

# Local path the Hinen OAuth page redirects back to. Namespaced with "_solar" so
# it never collides with the official hinen_power integration's /auth/hinen/callback.
CALLBACK_PATH = "/auth/hinen_solar/callback"

# Where users apply for their own Client ID / Client Secret.
DEVELOPER_PORTAL_URL = "https://developer.celinksmart.com/en_US/feedback"

# Config-flow field keys.
CONF_AUTH_LANGUAGE = "auth_language"
CONF_REDIRECT_BASE = "redirect_base"

# OAuth grant types (sent as query params; string form matches the API).
GRANT_TYPE_AUTHORIZATION_CODE = "1"
GRANT_TYPE_REFRESH_TOKEN = "2"

# Extra fields we persist alongside the standard OAuth token dict.
TOKEN_HOST = "host"
TOKEN_REGION_CODE = "region_code"
TOKEN_CLIENT_ID = "client_id"
TOKEN_CLIENT_SECRET = "client_secret"

# Languages offered on the Hinen OAuth authorization page.
SUPPORTED_LANGUAGES = {
    "en_US": "English",
    "zh_CN": "简体中文",
}

# Default update interval (seconds).
DEFAULT_SCAN_INTERVAL = 60

# Device status codes.
STATUS_OFFLINE = 0
STATUS_ONLINE = 1
STATUS_HIBERNATE = 2

# Device-level fault/alarm state (`alertStatus`) — device value -> option slug.
# Values match the legacy `hinen_power` integration (0 NORMAL / 1 ALARM / 2 ERROR).
# Slugs, not labels: automations bind to these (see WORK_MODE_OPTIONS below).
ALERT_STATUS_NORMAL = 0
ALERT_STATUS_OPTIONS = {
    0: "normal",
    1: "alarm",
    2: "error",
}

# Writable work-mode enum (WorkModeSetting property) — device value -> HA option slug.
# The slugs deliberately match the legacy `hinen_power` integration's for the same
# device values, so automations written against it keep working unchanged. Friendly
# labels live in translations, so re-wording one is not a breaking change for
# automations the way changing an option value is.
WORK_MODE_OPTIONS = {
    10: "self_consumption",
    11: "battery_priority",
    12: "grid_priority",
    13: "time_period",
    14: "power_keeping",
}
