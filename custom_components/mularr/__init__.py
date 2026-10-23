"""The Mularr integration."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_integration

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_API_KEY,
    CONF_SSL,
    CONF_SCAN_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_SSL,
    DEFAULT_SCAN_INTERVAL,
    PLATFORMS,
)
from .coordinator import MularrDataUpdateCoordinator
from .mularr_api import MularrApiClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Mularr from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    api_key = entry.data.get(CONF_API_KEY)
    use_ssl = entry.data.get(CONF_SSL, DEFAULT_SSL)

    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )

    session = async_get_clientsession(hass)
    client = MularrApiClient(
        host=host,
        port=port,
        api_key=api_key,
        use_ssl=use_ssl,
        session=session,
    )

    integration_version: str | None = None
    try:
        integration = await async_get_integration(hass, DOMAIN)
        integration_version = integration.version
    except Exception:
        pass

    coordinator = MularrDataUpdateCoordinator(
        hass=hass,
        client=client,
        update_interval=scan_interval,
        version=integration_version,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    coordinator: MularrDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    coordinator.update_interval = coordinator.default_interval = coordinator.update_interval.__class__(
        seconds=scan_interval
    )
    await coordinator.async_request_refresh()
