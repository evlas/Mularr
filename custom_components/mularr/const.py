"""Constants for the Mularr integration."""
from typing import Final
from homeassistant.const import Platform

DOMAIN: Final = "mularr"

CONF_HOST: Final = "host"
CONF_PORT: Final = "port"
CONF_API_KEY: Final = "api_key"
CONF_SSL: Final = "ssl"
CONF_VERIFY_SSL: Final = "verify_ssl"
CONF_SCAN_INTERVAL: Final = "scan_interval"

DEFAULT_PORT: Final = 8940
DEFAULT_SCAN_INTERVAL: Final = 10
DEFAULT_SSL: Final = False
DEFAULT_VERIFY_SSL: Final = True

PLATFORMS: Final = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.SWITCH,
]
