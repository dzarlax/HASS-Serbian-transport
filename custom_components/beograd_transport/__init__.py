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