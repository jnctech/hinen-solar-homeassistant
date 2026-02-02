"""Constants for the Hinen Solar integration."""

DOMAIN = "hinen"

# OAuth2 endpoints
OAUTH_AUTHORIZE_URL = "https://global.knowledge.celinksmart.com/#/auth"
OAUTH_TOKEN_URL = "https://global.iot-api.celinksmart.com/iot-global/open-platforms/auth/token"

# Data center hosts
HOSTS = {
    "ap": "https://ap.iot-api.celinksmart.com",  # Asia Pacific (Singapore)
    "au": "https://au.iot-api.celinksmart.com",  # Australia (Sydney)
    "eu": "https://eu.iot-api.celinksmart.com",  # Europe (London)
}

# Default update interval
DEFAULT_SCAN_INTERVAL = 60  # seconds

# Grant types
GRANT_TYPE_AUTHORIZATION_CODE = 1
GRANT_TYPE_REFRESH_TOKEN = 2

# Device status
STATUS_OFFLINE = 0
STATUS_ONLINE = 1
STATUS_HIBERNATE = 2
