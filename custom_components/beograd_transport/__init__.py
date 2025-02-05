"""The Serbian Transport integration."""
import os
import shutil
import logging
from pathlib import Path
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components import frontend

from .const import DOMAIN, NAME, VERSION

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[str] = []

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Serbian Transport component."""
    
    return True



async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Serbian Transport from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Copy files to www/community directory
    www_path = hass.config.path("www")
    www_community = hass.config.path("www", "community")
    www_component = hass.config.path("www", "community", DOMAIN)
    assets_path = os.path.join(www_component, "assets")
    
    for path in [www_path, www_community, www_component, assets_path]:
        if not os.path.exists(path):
            os.makedirs(path)
    
    # Copy component files
    local_www = os.path.join(os.path.dirname(__file__), "www")
    if os.path.exists(local_www):
        # Copy root files
        for file in os.listdir(local_www):
            src = os.path.join(local_www, file)
            if os.path.isfile(src):
                dst = os.path.join(www_component, file)
                shutil.copy2(src, dst)
        
        # Copy assets directory
        local_assets = os.path.join(local_www, "assets")
        if os.path.exists(local_assets):
            for file in os.listdir(local_assets):
                src = os.path.join(local_assets, file)
                if os.path.isfile(src):
                    dst = os.path.join(assets_path, file)
                    shutil.copy2(src, dst)
    
    if entry.options.get("add_sidebar", True):
        _LOGGER.debug("Registering panel for Serbian Transport")
        frontend.async_remove_panel(hass, "beograd_transport")
        
        frontend.async_register_built_in_panel(
            hass,
            "custom",
            sidebar_title=NAME,
            sidebar_icon="mdi:bus",
            frontend_url_path="beograd_transport",
            require_admin=False,
            config={
                "_panel_custom": {
                    "name": "beograd_transport",
                    "module_url": "/local/community/beograd_transport/dashboard.js",
                    "embed_iframe": False,
                    "trust_external": True
                }
            }
        )

    # Store configuration
    hass.data[DOMAIN][entry.entry_id] = {
        "options": entry.options,
        "version": VERSION
    }

    # Register update listener
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if entry.options.get("add_sidebar", True):
        frontend.async_remove_panel(hass, "beograd_transport")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)