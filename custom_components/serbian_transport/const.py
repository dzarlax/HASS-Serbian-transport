"""Constants for the Serbian Transport integration."""
from typing import Final

DOMAIN: Final = "serbian_transport"
PLATFORMS: Final[list[str]] = ["sensor"]

# Configuration constants
CONF_STATION_ID = "station_id"
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 300  # 5 minutes

# Service constants
ATTR_NEXT_DEPARTURE = "next_departure"
ATTR_LINE_NUMBER = "line_number"
ATTR_DESTINATION = "destination"