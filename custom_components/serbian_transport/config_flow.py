"""Config flow for Serbian Transport integration."""
from __future__ import annotations

import voluptuous as vol
from typing import Any, Final

# Import these at module level
from homeassistant.config_entries import ConfigFlow, ConfigEntry, OptionsFlow
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN  # Import from const.py instead of __init__.py

class SerbianTransportConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Serbian Transport."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Use location from HA config if not specified
            latitude = user_input.get(CONF_LATITUDE, self.hass.config.latitude)
            longitude = user_input.get(CONF_LONGITUDE, self.hass.config.longitude)
            search_rad = user_input.get("search_rad", 1000)

            return self.async_create_entry(
                title="Serbian Transport",
                data={
                    CONF_LATITUDE: latitude,
                    CONF_LONGITUDE: longitude,
                    "search_rad": search_rad,
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_LATITUDE,
                        default=self.hass.config.latitude
                    ): cv.latitude,
                    vol.Required(
                        CONF_LONGITUDE,
                        default=self.hass.config.longitude
                    ): cv.longitude,
                    vol.Required(
                        "search_rad",
                        default=1000
                    ): vol.All(
                        vol.Coerce(int),
                        vol.Range(min=100, max=20000)
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> SerbianTransportOptionsFlow:
        """Get the options flow for this handler."""
        return SerbianTransportOptionsFlow(config_entry)


class SerbianTransportOptionsFlow(OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "search_rad",
                        default=self.config_entry.options.get("search_rad", 1000)
                    ): vol.All(
                        vol.Coerce(int),
                        vol.Range(min=100, max=20000)
                    ),
                }
            )
        )