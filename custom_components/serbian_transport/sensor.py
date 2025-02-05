import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .coordinator import TransportStationsCoordinator
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    """Поддержка настройки через configuration.yaml."""
    lat = config.get("lat", hass.config.latitude)
    lon = config.get("lon", hass.config.longitude)
    rad = config.get("search_rad", 1000)

    coordinator = TransportStationsCoordinator(hass, lat, lon, rad)
    await coordinator.async_config_entry_first_refresh()

    # Пример создания одного сенсора
    sensors = [
        TransportStationsCountSensor(coordinator, "Transport Stations Count"),
    ]
    add_entities(sensors, True)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Поддержка настройки через UI (если используете config_flow)."""
    lat = hass.config.latitude
    lon = hass.config.longitude
    rad = entry.data["search_rad"]  # Using the key from config_flow


    coordinator = TransportStationsCoordinator(hass, lat, lon, rad)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        TransportStationsCountSensor(coordinator, "Transport Stations Count"),
    ]
    async_add_entities(sensors, True)

class TransportStationsCountSensor(SensorEntity):
    """Сенсор, который показывает количество ближайших остановок."""

    def __init__(self, coordinator, name):
        self._coordinator = coordinator
        self._attr_name = name
        self._state = None

    @property
    def should_poll(self):
        """Отключаем опрос, используем Coordinator."""
        return False

    @property
    def state(self):
        """Возвращаем текущее состояние - количество остановок."""
        if self._coordinator.data is None:
            return None
        return len(self._coordinator.data)

    @property
    def extra_state_attributes(self):
        """Дополнительные атрибуты (можем положить, например, список остановок)."""
        if not self._coordinator.data:
            return {}
        return {
            "stations": self._coordinator.data,
        }

    async def async_added_to_hass(self):
        """Вызывается при добавлении сенсора в HASS."""
        self._coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Вызывается при удалении сенсора из HASS."""
        self._coordinator.async_remove_listener(self.async_write_ha_state)

    @property
    def unique_id(self):
        return "transport_stations_count"

    @property
    def available(self):
        """Сенсор доступен, если есть данные (или до ошибок API)."""
        return self._coordinator.last_update_success