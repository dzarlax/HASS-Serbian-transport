import asyncio
import logging
import aiohttp
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

SERVER_IP = "https://transport-api.dzarlax.dev"

async def fetch_stations(session, lat, lon, rad):
    """Запрос к вашему API, возвращает список остановок."""
    # Пример — нужно адаптировать под ваш реальный endpoint
    # Можно ходить по нескольким городам (как у вас BG, NS, NIS) в цикле
    url = f"{SERVER_IP}/api/stations/bg/all"
    params = {"lat": lat, "lon": lon, "rad": rad}
    try:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                raise UpdateFailed(f"Error fetching data: {resp.status}")
            data = await resp.json()
            return data
    except Exception as e:
        raise UpdateFailed(f"Exception while fetching: {e}")

class TransportStationsCoordinator(DataUpdateCoordinator):
    """Координатор для получения и кэширования данных об остановках."""

    def __init__(self, hass, lat, lon, rad):
        """Инициализация."""
        super().__init__(
            hass,
            _LOGGER,
            name="transport_stations_coordinator",
            update_interval=timedelta(seconds=30),  # Частота обновления
        )
        self.lat = lat
        self.lon = lon
        self.rad = rad

    async def _async_update_data(self):
        """Функция, которую вызывает HA для обновления данных."""
        # Здесь пишем логику обращения к API
        async with aiohttp.ClientSession() as session:
            stations = await fetch_stations(session, self.lat, self.lon, self.rad)
            return stations