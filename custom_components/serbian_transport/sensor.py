"""Serbian Transport sensor platform."""
import logging
from typing import Dict, Any, Optional
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .coordinator import TransportStationsCoordinator
from .const import (
    DOMAIN, 
    CONF_SEARCH_RADIUS, 
    DEFAULT_SEARCH_RADIUS,
    SENSOR_TYPES,
    ATTR_STATIONS,
    ATTR_STATION_COUNT
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant, 
    config: Dict[str, Any], 
    add_entities: AddEntitiesCallback, 
    discovery_info: Optional[Dict[str, Any]] = None
) -> None:
    """Set up sensors from configuration.yaml (legacy support)."""
    _LOGGER.warning("Configuration via configuration.yaml is deprecated. Please use the UI configuration.")
    
    lat = config.get("lat", hass.config.latitude)
    lon = config.get("lon", hass.config.longitude) 
    rad = config.get(CONF_SEARCH_RADIUS, DEFAULT_SEARCH_RADIUS)

    if lat is None or lon is None:
        _LOGGER.error("Latitude and longitude must be configured")
        return

    coordinator = TransportStationsCoordinator(hass, lat, lon, rad)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        TransportStationsCountSensor(coordinator),
    ]
    add_entities(sensors, True)

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensors from a config entry."""
    # Support for both new and legacy config keys for backward compatibility
    lat = entry.data.get("latitude") or entry.data.get(CONF_LATITUDE, hass.config.latitude)
    lon = entry.data.get("longitude") or entry.data.get(CONF_LONGITUDE, hass.config.longitude)
    rad = entry.data.get(CONF_SEARCH_RADIUS) or entry.data.get("search_rad", DEFAULT_SEARCH_RADIUS)

    if lat is None or lon is None:
        _LOGGER.error("Latitude and longitude must be configured")
        return

    _LOGGER.debug("Setting up sensors for coordinates (%.6f, %.6f) with radius %dm", lat, lon, rad)
    _LOGGER.debug("Entry data keys: %s", list(entry.data.keys()))
    _LOGGER.debug("Entry data values: %s", entry.data)

    coordinator = TransportStationsCoordinator(hass, lat, lon, rad)
    
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as e:
        _LOGGER.error("Failed to fetch initial data: %s", e)
        # Continue setup even if initial fetch fails - coordinator will retry

    sensors = [
        TransportStationsCountSensor(coordinator),
        TransportNextDepartureSensor(coordinator),
    ]
    async_add_entities(sensors, True)

class TransportStationsCountSensor(SensorEntity):
    """Sensor that shows the count of nearby transport stations."""

    _attr_has_entity_name = True
    _attr_name = "Stations Count"
    _attr_icon = "mdi:bus-stop"
    _attr_native_unit_of_measurement = "stations"

    def __init__(self, coordinator: TransportStationsCoordinator) -> None:
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_stations_count"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "transport_stations")},
            "name": "Serbian Transport",
            "manufacturer": "Serbian Transport Integration",
            "model": "Transport Monitor",
        }

    @property
    def should_poll(self) -> bool:
        """Disable polling - we use coordinator."""
        return False

    @property
    def native_value(self) -> Optional[int]:
        """Return the number of stations."""
        return self._coordinator.station_count

    @property
    def available(self) -> bool:
        """Return True if sensor is available."""
        return self._coordinator.last_update_success

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes."""
        if not self._coordinator.has_data:
            _LOGGER.debug("No coordinator data available for stations count sensor")
            return {}
        
        stations_data = self._coordinator.data
        _LOGGER.debug("Stations count sensor returning %d stations: %s", 
                     len(stations_data) if stations_data else 0, 
                     [s.get('name', 'Unknown') for s in stations_data[:3]] if stations_data else [])
        
        return {
            ATTR_STATIONS: stations_data,
            ATTR_STATION_COUNT: self._coordinator.station_count,
            "last_update_success": self._coordinator.last_update_success,
            "search_radius": self._coordinator.rad,
            "coordinates": f"{self._coordinator.lat:.6f}, {self._coordinator.lon:.6f}"
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        await super().async_added_to_hass()
        self._coordinator.async_add_listener(self._handle_coordinator_update)

    async def async_will_remove_from_hass(self) -> None:
        """Unregister callbacks."""
        self._coordinator.async_remove_listener(self._handle_coordinator_update)
        await super().async_will_remove_from_hass()


class TransportNextDepartureSensor(SensorEntity):
    """Sensor that shows the next departure time in minutes."""

    _attr_has_entity_name = True
    _attr_name = "Next Departure"
    _attr_icon = "mdi:bus-clock"
    _attr_native_unit_of_measurement = "min"

    def __init__(self, coordinator: TransportStationsCoordinator) -> None:
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_next_departure"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "transport_stations")},
            "name": "Serbian Transport",
            "manufacturer": "Serbian Transport Integration",
            "model": "Transport Monitor",
        }

    @property
    def should_poll(self) -> bool:
        """Disable polling - we use coordinator."""
        return False

    @property
    def native_value(self) -> Optional[int]:
        """Return the time until next departure in minutes."""
        if not self._coordinator.has_data:
            return None
            
        min_departure = None
        for station in self._coordinator.data:
            vehicles = station.get("vehicles", [])
            for vehicle in vehicles:
                seconds_left = vehicle.get("secondsLeft")
                if seconds_left is not None:
                    minutes = max(1, int(seconds_left / 60))  # At least 1 minute
                    if min_departure is None or minutes < min_departure:
                        min_departure = minutes
                        
        return min_departure

    @property
    def available(self) -> bool:
        """Return True if sensor is available."""
        return self._coordinator.last_update_success and self._coordinator.has_data

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes."""
        if not self._coordinator.has_data:
            return {}
            
        departures = []
        for station in self._coordinator.data:
            vehicles = station.get("vehicles", [])
            for vehicle in vehicles:
                seconds_left = vehicle.get("secondsLeft")
                if seconds_left is not None:
                    departures.append({
                        "station": station.get("name", "Unknown"),
                        "line": vehicle.get("lineNumber", "Unknown"),
                        "destination": vehicle.get("lineName", "Unknown"),
                        "minutes": max(1, int(seconds_left / 60)),
                        "stations_between": vehicle.get("stationsBetween", 0)
                    })
        
        # Sort by departure time
        departures.sort(key=lambda x: x["minutes"])
        
        return {
            "all_departures": departures[:10],  # Limit to 10 nearest
            "departure_count": len(departures),
            "last_update_success": self._coordinator.last_update_success,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        await super().async_added_to_hass()
        self._coordinator.async_add_listener(self._handle_coordinator_update)

    async def async_will_remove_from_hass(self) -> None:
        """Unregister callbacks."""
        self._coordinator.async_remove_listener(self._handle_coordinator_update)
        await super().async_will_remove_from_hass()