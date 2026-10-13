"""Binary sensor platform for Mularr integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MularrDataUpdateCoordinator
from .entity import MularrEntity


@dataclass(frozen=True)
class MularrBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class describing Mularr binary sensor entities."""

    is_on_fn: Callable[[dict[str, Any]], bool] | None = None
    attrs_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None


BINARY_SENSOR_TYPES: tuple[MularrBinarySensorEntityDescription, ...] = (
    MularrBinarySensorEntityDescription(
        key="ed2k_connected",
        translation_key="ed2k_connected",
        name="ED2K Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        is_on_fn=lambda data: bool(
            data.get("status", {}).get("connectionState", {}).get("ed2kConnected")
        ),
    ),
    MularrBinarySensorEntityDescription(
        key="kad_connected",
        translation_key="kad_connected",
        name="KAD Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        is_on_fn=lambda data: bool(
            data.get("status", {}).get("connectionState", {}).get("kadConnected")
        ),
    ),
    MularrBinarySensorEntityDescription(
        key="kad_firewalled",
        translation_key="kad_firewalled",
        name="KAD Firewalled",
        device_class=BinarySensorDeviceClass.PROBLEM,
        is_on_fn=lambda data: bool(
            data.get("status", {}).get("connectionState", {}).get("kadFirewalled")
        ),
    ),
    MularrBinarySensorEntityDescription(
        key="vpn_status",
        translation_key="vpn_status",
        name="VPN Active",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        is_on_fn=lambda data: bool(
            data.get("system", {}).get("vpn", {}).get("enabled")
            and data.get("system", {}).get("vpn", {}).get("status") in ("running", "connected")
        ),
        attrs_fn=lambda data: data.get("system", {}).get("vpn") or {},
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Mularr binary sensor platform."""
    coordinator: MularrDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        MularrBinarySensor(coordinator, entry.entry_id, description)
        for description in BINARY_SENSOR_TYPES
    )


class MularrBinarySensor(MularrEntity, BinarySensorEntity):
    """Representation of a Mularr binary sensor."""

    entity_description: MularrBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: MularrDataUpdateCoordinator,
        entry_id: str,
        description: MularrBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, entry_id, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        if self.entity_description.is_on_fn:
            return self.entity_description.is_on_fn(self.coordinator.data)
        return False

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the extra state attributes."""
        if self.entity_description.attrs_fn:
            return self.entity_description.attrs_fn(self.coordinator.data)
        return {}
