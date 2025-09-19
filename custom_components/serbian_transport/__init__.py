"""The Serbian Transport integration."""
import logging
import os
import shutil
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.frontend import add_extra_js_url

_LOGGER = logging.getLogger(__name__)

DOMAIN = "serbian_transport"
PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config) -> bool:
    """Initialize through configuration.yaml."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Serbian Transport from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create www/community directory if it doesn't exist
    www_path = hass.config.path("www")
    www_community = hass.config.path("www", "community")
    www_component = hass.config.path("www", "community", DOMAIN)
    
    for path in [www_path, www_community, www_component]:
        if not os.path.exists(path):
            os.makedirs(path)
    
    # Copy component files from www directory
    local_www = os.path.join(os.path.dirname(__file__), "www")
    if os.path.exists(local_www):
        for file in os.listdir(local_www):
            src = os.path.join(local_www, file)
            dst = os.path.join(www_component, file)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                _LOGGER.debug("Copied %s to %s", src, dst)

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