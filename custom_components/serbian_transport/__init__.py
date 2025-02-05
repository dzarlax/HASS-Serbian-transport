"""The Serbian Transport integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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

    # Регистрация статического пути
    hass.http.register_static_path(
        f"/local/community/{DOMAIN}/transport-card.js",
        hass.config.path(f"www/community/{DOMAIN}/transport-card.js"),
        cache_headers=True
    )

    # Регистрация ресурса в Lovelace
    try:
        await async_register_resource(
            hass,
            "module",
            f"/local/community/{DOMAIN}/transport-card.js"
        )
    except Exception as e:
        _LOGGER.error("Failed to register Lovelace resource: %s", e)

    # Сохранение конфигурации
    hass.data[DOMAIN][entry.entry_id] = {
        "config": entry.data,
        "options": entry.options,
    }

    # Загрузка платформ
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok