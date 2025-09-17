"""The Serbian Transport integration."""
import logging
import os
import shutil
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE

from .const import CONF_SEARCH_RADIUS

_LOGGER = logging.getLogger(__name__)

DOMAIN = "serbian_transport"
PLATFORMS = ["sensor"]


def _setup_frontend_files_sync(hass: HomeAssistant) -> None:
    """Set up frontend files synchronously (to be run in executor)."""
    # Create www/community directory if it doesn't exist
    www_path = hass.config.path("www")
    www_community = hass.config.path("www", "community")
    www_component = hass.config.path("www", "community", DOMAIN)
    
    for path in [www_path, www_community, www_component]:
        if not os.path.exists(path):
            os.makedirs(path)
            _LOGGER.debug("Created directory: %s", path)
    
    # Copy component files from www directory
    local_www = os.path.join(os.path.dirname(__file__), "www")
    if os.path.exists(local_www):
        for file in os.listdir(local_www):
            src = os.path.join(local_www, file)
            dst = os.path.join(www_component, file)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                _LOGGER.debug("Copied %s to %s", src, dst)


async def _async_setup_frontend_files(hass: HomeAssistant) -> None:
    """Set up frontend files asynchronously."""
    await hass.async_add_executor_job(_setup_frontend_files_sync, hass)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry format to new format."""
    _LOGGER.debug("Migrating Serbian Transport from version %s", config_entry.version)
    
    if config_entry.version == 1:
        # Migrate from version 1 to version 2
        new_data = dict(config_entry.data)
        
        # Migrate search_rad to CONF_SEARCH_RADIUS
        if "search_rad" in new_data:
            new_data[CONF_SEARCH_RADIUS] = new_data.pop("search_rad")
            _LOGGER.debug("Migrated search_rad to %s", CONF_SEARCH_RADIUS)
        
        # Ensure we have the proper keys
        if CONF_LATITUDE not in new_data and "latitude" in new_data:
            new_data[CONF_LATITUDE] = new_data["latitude"]
        if CONF_LONGITUDE not in new_data and "longitude" in new_data:
            new_data[CONF_LONGITUDE] = new_data["longitude"]
        
        hass.config_entries.async_update_entry(config_entry, data=new_data, version=2)
        _LOGGER.info("Serbian Transport migration to version %s successful", 2)
    elif config_entry.version > 2:
        # Future versions - just log and continue
        _LOGGER.info("Serbian Transport config entry version %s is newer than expected", config_entry.version)
    else:
        # Version 2 or unknown versions
        _LOGGER.debug("Serbian Transport config entry version %s requires no migration", config_entry.version)
        
    return True

async def async_setup(hass: HomeAssistant, config) -> bool:
    """Initialize through configuration.yaml."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Serbian Transport from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create www/community directory and copy files asynchronously
    await _async_setup_frontend_files(hass)

    # Register static path and Lovelace resource
    url_path = f"/local/community/{DOMAIN}/transport-card.js"
    file_path = hass.config.path(f"www/community/{DOMAIN}/transport-card.js")
    
    await hass.http.async_register_static_paths([
        StaticPathConfig(url_path=url_path, path=file_path, cache_headers=True)
    ])

    # Register JS module
    add_extra_js_url(hass, url_path)  

    # Load platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Serbian Transport integration")
    
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        # Clean up any stored data for this entry
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id, None)
        _LOGGER.debug("Serbian Transport integration unloaded successfully")
    
    return unload_ok