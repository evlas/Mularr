"""Switch platform for Mularr integration."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MularrDataUpdateCoordinator
from .entity import MularrEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Mularr switch platform."""
    coordinator: MularrDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        MularrServerSwitch(
            coordinator,
            entry.entry_id,
            SwitchEntityDescription(
                key="server_connection",
                translation_key="server_connection",
                icon="mdi:server-network",
            ),
        )
    ])


class MularrServerSwitch(MularrEntity, SwitchEntity):
    """Switch to connect or disconnect from ED2K server."""

    entity_description: SwitchEntityDescription

    def __init__(
        self,
        coordinator: MularrDataUpdateCoordinator,
        entry_id: str,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, entry_id, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool:
        """Return true if connected to server."""
        return bool(
            self.coordinator.data.get("status", {})
            .get("connectionState", {})
            .get("ed2kConnected")
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Connect to server."""
        await self.coordinator.client.connect_server()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disconnect from server."""
        await self.coordinator.client.disconnect_server()
        await self.coordinator.async_request_refresh()
