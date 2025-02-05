import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "serbian_transport"
PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config) -> bool:
    """Инициализация через configuration.yaml."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Настройка через Config Flow."""
    hass.data.setdefault(DOMAIN, {})
    
    # Загрузка платформ (сенсоров)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Выгрузка Config Entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Register custom card
    hass.http.register_static_path(
        f"/hacsfiles/{DOMAIN}/transport-card.js",
        hass.config.path(f"custom_components/{DOMAIN}/www/transport-card.js"),
        True
    )
    
    # Add to frontend resources
    hass.components.frontend.async_register_built_in_panel(
        "custom",
        "transport-card",
        require_admin=False,
        js_url=f"/hacsfiles/{DOMAIN}/transport-card.js",
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True