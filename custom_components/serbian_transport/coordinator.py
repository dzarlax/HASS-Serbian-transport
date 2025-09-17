import asyncio
import logging
import aiohttp
from datetime import timedelta
from typing import Dict, List, Any, Optional
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import (
    DEFAULT_API_TIMEOUT,
    DEFAULT_MAX_RETRIES,
    DEFAULT_API_BASE_URL,
    DEFAULT_UPDATE_INTERVAL
)

_LOGGER = logging.getLogger(__name__)


def determine_city_by_coordinates(lat: float, lon: float) -> str:
    """
    Determine the most likely city based on coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        City code ('bg', 'ns', 'nis')
    """
    # Approximate coordinates for Serbian cities
    # Belgrade: 44.8176, 20.4633
    # Novi Sad: 45.2396, 19.8227  
    # Niš: 43.3209, 21.8958
    
    cities = {
        'bg': (44.8176, 20.4633),   # Belgrade
        'ns': (45.2396, 19.8227),   # Novi Sad
        'nis': (43.3209, 21.8958),  # Niš
    }
    
    min_distance = float('inf')
    closest_city = 'bg'  # Default to Belgrade
    
    for city_code, (city_lat, city_lon) in cities.items():
        # Simple distance calculation (not precise, but good enough for city determination)
        distance = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_city = city_code
    
    _LOGGER.debug("Determined city %s for coordinates (%.6f, %.6f)", closest_city, lat, lon)
    return closest_city


async def fetch_stations(
    session: aiohttp.ClientSession, 
    lat: float, 
    lon: float, 
    rad: int, 
    timeout: int = DEFAULT_API_TIMEOUT,
    retries: int = DEFAULT_MAX_RETRIES
) -> List[Dict[str, Any]]:
    """
    Fetch transport stations from API based on coordinates with improved error handling.
    
    Args:
        session: aiohttp client session
        lat: Latitude coordinate
        lon: Longitude coordinate
        rad: Search radius in meters
        timeout: Request timeout in seconds
        retries: Number of retry attempts
        
    Returns:
        List of station data dictionaries
        
    Raises:
        UpdateFailed: When all retry attempts fail
    """
    # API endpoints for finding nearby stations based on coordinates 
    # Try city-specific endpoints in order of preference based on determined location
    determined_city = determine_city_by_coordinates(lat, lon)
    
    endpoints_to_try = [
        f"{DEFAULT_API_BASE_URL}/api/stations/{determined_city}/all",  # Auto-determined city endpoint
        f"{DEFAULT_API_BASE_URL}/api/stations/bg/all",  # Fallback to Belgrade endpoint
        f"{DEFAULT_API_BASE_URL}/api/stations/ns/all",  # Fallback to Novi Sad endpoint  
        f"{DEFAULT_API_BASE_URL}/api/stations/nis/all", # Fallback to Nis endpoint
    ]
    
    # Remove duplicates while preserving order
    endpoints_to_try = list(dict.fromkeys(endpoints_to_try))
    
    params = {"lat": lat, "lon": lon, "rad": rad}
    
    last_exception = None
    
    # Try each endpoint until one works
    for endpoint_idx, url in enumerate(endpoints_to_try):
        last_exception = None
        
        for attempt in range(retries + 1):
            try:
                _LOGGER.debug(
                    "Fetching stations (endpoint %d/%d, attempt %d/%d): %s with params %s", 
                    endpoint_idx + 1, len(endpoints_to_try), attempt + 1, retries + 1, url, params
                )
                
                timeout_config = aiohttp.ClientTimeout(total=timeout)
                async with session.get(url, params=params, timeout=timeout_config) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        _LOGGER.debug("Successfully fetched %d stations from %s", len(data) if data else 0, url)
                        if data:
                            _LOGGER.debug("Sample station data: %s", data[0] if len(data) > 0 else "No stations")
                        return data if data else []
                        
                    elif resp.status == 429:  # Rate limited
                        wait_time = 2 ** attempt  # Exponential backoff
                        _LOGGER.warning(
                            "Rate limited (endpoint %d, attempt %d/%d). Waiting %ds before retry", 
                            endpoint_idx + 1, attempt + 1, retries + 1, wait_time
                        )
                        if attempt < retries:
                            await asyncio.sleep(wait_time)
                            continue
                        last_exception = UpdateFailed(f"Rate limited after {retries + 1} attempts on {url}")
                        break  # Try next endpoint
                        
                    elif resp.status == 404:
                        _LOGGER.warning("API endpoint not found: %s (trying next endpoint)", url)
                        last_exception = UpdateFailed(f"API endpoint not found: {url}")
                        break  # Try next endpoint immediately
                        
                    elif resp.status >= 500:  # Server errors - retry
                        error_text = await resp.text()
                        _LOGGER.warning(
                            "Server error %d (endpoint %d, attempt %d/%d): %s", 
                            resp.status, endpoint_idx + 1, attempt + 1, retries + 1, error_text
                        )
                        if attempt < retries:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        last_exception = UpdateFailed(f"Server error {resp.status} after {retries + 1} attempts on {url}")
                        break  # Try next endpoint
                        
                    else:  # Client errors - try next endpoint
                        error_text = await resp.text()
                        _LOGGER.warning("Client error %d on %s: %s (trying next endpoint)", resp.status, url, error_text)
                        last_exception = UpdateFailed(f"Client error {resp.status} on {url}")
                        break  # Try next endpoint
                    
            except asyncio.TimeoutError:
                _LOGGER.warning(
                    "Request timeout (endpoint %d, attempt %d/%d) after %ds", 
                    endpoint_idx + 1, attempt + 1, retries + 1, timeout
                )
                last_exception = UpdateFailed(f"Request timeout after {timeout}s on {url}")
                if attempt < retries:
                    await asyncio.sleep(1)
                    continue
                else:
                    break  # Try next endpoint
                    
            except aiohttp.ClientError as e:
                _LOGGER.warning(
                    "Network error (endpoint %d, attempt %d/%d): %s", 
                    endpoint_idx + 1, attempt + 1, retries + 1, str(e)
                )
                last_exception = UpdateFailed(f"Network error: {e} on {url}")
                if attempt < retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    break  # Try next endpoint
                    
            except Exception as e:
                _LOGGER.error("Unexpected error on %s: %s", url, str(e), exc_info=True)
                last_exception = UpdateFailed(f"Unexpected error: {e} on {url}")
                break  # Try next endpoint
    
    # If we get here, all endpoints and retries failed
    raise last_exception or UpdateFailed("All endpoints and retry attempts failed")

class TransportStationsCoordinator(DataUpdateCoordinator):
    """Coordinator for fetching and caching transport station data."""

    def __init__(
        self, 
        hass: HomeAssistant, 
        lat: float, 
        lon: float, 
        rad: int,
        update_interval: int = DEFAULT_UPDATE_INTERVAL
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="transport_stations_coordinator",
            update_interval=timedelta(seconds=update_interval),
        )
        self.lat = lat
        self.lon = lon
        self.rad = rad
        self._last_successful_update = None

    async def _async_update_data(self) -> List[Dict[str, Any]]:
        """Fetch data from API with improved error handling."""
        _LOGGER.debug(
            "Updating transport data for coordinates (%.6f, %.6f) with radius %dm",
            self.lat, self.lon, self.rad
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                stations = await fetch_stations(session, self.lat, self.lon, self.rad)
                
                if stations:
                    self._last_successful_update = stations
                    _LOGGER.debug("Successfully updated %d stations", len(stations))
                else:
                    _LOGGER.warning("No stations found for given coordinates")
                    
                return stations
                
        except UpdateFailed as e:
            _LOGGER.error("Failed to update transport data: %s", e)
            
            # Return last successful data if available, otherwise re-raise
            if self._last_successful_update is not None:
                _LOGGER.info("Using cached data from last successful update")
                return self._last_successful_update
            raise

    @property
    def station_count(self) -> int:
        """Return the number of stations in current data."""
        return len(self.data) if self.data else 0

    @property
    def has_data(self) -> bool:
        """Return True if coordinator has any data."""
        return self.data is not None and len(self.data) > 0