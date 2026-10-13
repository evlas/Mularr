"""Base entity for Mularr integration."""
from __future__ import annotations

from typing import Any
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MularrDataUpdateCoordinator


class MularrEntity(CoordinatorEntity[MularrDataUpdateCoordinator]):
    """Defines a base Mularr entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MularrDataUpdateCoordinator,
        entry_id: str,
        unique_id_suffix: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_{unique_id_suffix}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry_id)},
            name=f"Mularr ({self.coordinator.client.host})",
            manufacturer="Mularr",
            model="aMule & P2P Web Automation",
            configuration_url=self.coordinator.client.base_url,
            sw_version="1.0.0",
        )
