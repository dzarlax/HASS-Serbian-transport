"""Constants for the Serbian Transport integration."""
from typing import Final, Dict

DOMAIN: Final = "serbian_transport"
PLATFORMS: Final[list[str]] = ["sensor"]

# API Configuration
DEFAULT_API_BASE_URL: Final = "https://transport-api.dzarlax.dev"
DEFAULT_API_TIMEOUT: Final = 10  # seconds
DEFAULT_MAX_RETRIES: Final = 3
DEFAULT_UPDATE_INTERVAL: Final = 30  # seconds

# Configuration constants
CONF_STATION_ID = "station_id"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_SEARCH_RADIUS = "search_rad"
DEFAULT_SEARCH_RADIUS = 1000  # meters

# Service constants
ATTR_NEXT_DEPARTURE = "next_departure"
ATTR_LINE_NUMBER = "line_number"
ATTR_DESTINATION = "destination"
ATTR_STATIONS = "stations"
ATTR_STATION_COUNT = "station_count"

# API Endpoints - unified endpoint for all cities based on coordinates
API_ENDPOINTS: Final[Dict[str, str]] = {
    "unified": DEFAULT_API_BASE_URL  # Single endpoint that handles all cities
}

# Sensor types
SENSOR_TYPES: Final[Dict[str, Dict[str, str]]] = {
    "stations_count": {
        "name": "Transport Stations Count",
        "icon": "mdi:bus-stop",
        "unit": "stations"
    },
    "next_departure": {
        "name": "Next Departure",
        "icon": "mdi:bus-clock", 
        "unit": "minutes"
    }
}