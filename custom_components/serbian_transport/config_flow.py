"""Config flow for Transport Stations Integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
import homeassistant.helpers.config_validation as cv

# Импортируйте DOMAIN из вашего __init__.py (или отдельно из const.py)
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

class TransportStationsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example Config Flow для транспортных остановок."""

    VERSION = 1  # Версия схемы конфигурации

    async def async_step_user(self, user_input=None):
        """Первый (и единственный) шаг настройки через UI."""
        errors = {}

        if user_input is not None:
            # При желании можно добавить валидацию, например, на корректность координат
            latitude = user_input[CONF_LATITUDE]
            longitude = user_input[CONF_LONGITUDE]
            search_rad = user_input["search_rad"]

            # Проверим, не установлена ли уже интеграция с такими же параметрами
            unique_id = f"{latitude}_{longitude}_{search_rad}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Transport Stations",
                data={
                    CONF_LATITUDE: latitude,
                    CONF_LONGITUDE: longitude,
                    "search_rad": search_rad
                }
            )

        # Значения по умолчанию возьмём из глобальных настроек HA, если есть
        default_lat = self.hass.config.latitude or 44.7866
        default_lon = self.hass.config.longitude or 20.4489

        data_schema = vol.Schema({
            vol.Required(CONF_LATITUDE, default=default_lat): cv.latitude,
            vol.Required(CONF_LONGITUDE, default=default_lon): cv.longitude,
            vol.Required("search_rad", default=100): vol.All(vol.Coerce(int), vol.Range(min=100, max=20000))
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )