"""The Serbian Transport integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.http import StaticPathConfig


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
    await hass.http.async_register_static_paths([StaticPathConfig("/local/community/serbian_transport/transport-card.js", "/config/www/community/serbian_transport/transport-card.js", True)])(
        f"/local/community/{DOMAIN}/transport-card.js",
        hass.config.path(f"www/community/{DOMAIN}/transport-card.js"),
        cache_headers=True
    )

    # Ручная регистрация ресурса в Lovelace
    if "lovelace_resources" in hass.data:
        resources = hass.data["lovelace_resources"]
        resource_url = f"/local/community/{DOMAIN}/transport-card.js"
        if not any(res["url"] == resource_url for res in resources):
            resources.append({"type": "module", "url": resource_url})
            _LOGGER.info("Registered Lovelace resource: %s", resource_url)

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