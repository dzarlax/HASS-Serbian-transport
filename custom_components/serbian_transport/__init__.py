"""The Serbian Transport integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.components.http.static_path import static_path_from_config
from homeassistant.components.lovelace.resources import async_register_resource

_LOGGER = logging.getLogger(__name__)

DOMAIN = "serbian_transport"
PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config) -> bool:
    """Initialize through configuration.yaml."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Serbian Transport from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Register static path using static_path_from_config
    static_path = static_path_from_config(
        url_path=f"/hacsfiles/{DOMAIN}/transport-card.js",
        path=hass.config.path(f"custom_components/{DOMAIN}/www/transport-card.js"),
        cache_headers=True
    )
    
    await hass.http.async_register_static_path(static_path)
    
    # Register as a Lovelace resource
    try:
        await async_register_resource(
            hass,
            "module",
            f"/hacsfiles/{DOMAIN}/transport-card.js"
        )
    except Exception as e:
        _LOGGER.error("Failed to register Lovelace resource: %s", e)

    # Store configuration
    hass.data[DOMAIN][entry.entry_id] = {
        "config": entry.data,
        "options": entry.options,
    }

    # Load platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        # Remove static path
        try:
            await hass.http.async_remove_static_path(f"/hacsfiles/{DOMAIN}/transport-card.js")
        except Exception as e:
            _LOGGER.error("Failed to remove static path: %s", e)
    return unload_ok