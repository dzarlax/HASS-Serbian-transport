"""The Serbian Transport integration."""
import logging
import os
import shutil
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.http import StaticPathConfig
from homeassistant.helpers.resources import async_register_resource

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

    # Register static path
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            url_path=f"/local/community/{DOMAIN}/transport-card.js",
            path=hass.config.path(f"www/community/{DOMAIN}/transport-card.js"),
            cache_headers=True
        )
    ])

    # Register Lovelace resource
    if "lovelace_resources" in hass.data:
        resources = hass.data["lovelace_resources"]
        resource_url = f"/local/community/{DOMAIN}/transport-card.js"
        if not any(res["url"] == resource_url for res in resources):
            resources.append({"type": "module", "url": resource_url})
            _LOGGER.info("Registered Lovelace resource: %s", resource_url)

    # Store configuration
    hass.data[DOMAIN][entry.entry_id] = {
        "config": entry.data,
        "options": entry.options,
    }

    # Register Lovelace resource
    await async_register_resource(
        hass,
        "module",
        f"/local/community/{DOMAIN}/transport-card.js",
        {DOMAIN}
    )

    # Load platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True