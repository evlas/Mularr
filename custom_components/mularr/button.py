"""Button platform for Mularr integration."""
from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MularrDataUpdateCoordinator
from .entity import MularrEntity


@dataclass(frozen=True)
class MularrButtonEntityDescription(ButtonEntityDescription):
    """Class describing Mularr button entities."""

    press_action: Callable[[MularrDataUpdateCoordinator], Coroutine[Any, Any, Any]] | None = None


BUTTON_TYPES: tuple[MularrButtonEntityDescription, ...] = (
    MularrButtonEntityDescription(
        key="restart_daemon",
        translation_key="restart_daemon",
        name="Restart Daemon",
        icon="mdi:restart",
        press_action=lambda coord: coord.client.restart_daemon(),
    ),
    MularrButtonEntityDescription(
        key="clear_completed",
        translation_key="clear_completed",
        name="Clear Completed Transfers",
        icon="mdi:broom",
        press_action=lambda coord: coord.client.clear_completed(),
    ),
    MularrButtonEntityDescription(
        key="connect_server",
        translation_key="connect_server",
        name="Connect to Server",
        icon="mdi:server-network",
        press_action=lambda coord: coord.client.connect_server(),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Mularr button platform."""
    coordinator: MularrDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        MularrButton(coordinator, entry.entry_id, description)
        for description in BUTTON_TYPES
    )


class MularrButton(MularrEntity, ButtonEntity):
    """Representation of a Mularr button entity."""

    entity_description: MularrButtonEntityDescription

    def __init__(
        self,
        coordinator: MularrDataUpdateCoordinator,
        entry_id: str,
        description: MularrButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator, entry_id, description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Handle button press."""
        if self.entity_description.press_action:
            await self.entity_description.press_action(self.coordinator)
            await self.coordinator.async_request_refresh()
