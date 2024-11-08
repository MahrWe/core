"""The Nord Pool component."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util

from .const import DOMAIN, PLATFORMS
from .coordinator import NordPoolDataUpdateCoordinator
from .services import async_setup_services

type NordPoolConfigEntry = ConfigEntry[NordPoolDataUpdateCoordinator]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Habitica service."""

    async_setup_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: NordPoolConfigEntry) -> bool:
    """Set up Nord Pool from a config entry."""

    coordinator = NordPoolDataUpdateCoordinator(hass, entry)
    await coordinator.fetch_data(dt_util.utcnow())
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: NordPoolConfigEntry) -> bool:
    """Unload Nord Pool config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
