"""Sensor platform for Mularr integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfDataRate,
    UnitOfInformation,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MularrDataUpdateCoordinator
from .entity import MularrEntity


@dataclass(frozen=True)
class MularrSensorEntityDescription(SensorEntityDescription):
    """Class describing Mularr sensor entities."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None
    attrs_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None


SENSOR_TYPES: tuple[MularrSensorEntityDescription, ...] = (
    MularrSensorEntityDescription(
        key="download_speed",
        translation_key="download_speed",
        name="Download Speed",
        device_class=SensorDeviceClass.DATA_RATE,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("status", {}).get("downloadSpeed", 0),
    ),
    MularrSensorEntityDescription(
        key="upload_speed",
        translation_key="upload_speed",
        name="Upload Speed",
        device_class=SensorDeviceClass.DATA_RATE,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("status", {}).get("uploadSpeed", 0),
    ),
    MularrSensorEntityDescription(
        key="id_status",
        translation_key="id_status",
        name="ID Status",
        icon="mdi:network",
        value_fn=lambda data: "HighID" if data.get("status", {}).get("isHighID") else "LowID",
    ),
    MularrSensorEntityDescription(
        key="connected_server",
        translation_key="connected_server",
        name="Connected Server",
        icon="mdi:server-network",
        value_fn=lambda data: (
            data.get("status", {}).get("connectedServer", {}).get("name")
            if data.get("status", {}).get("connectedServer")
            else "Disconnected"
        ),
        attrs_fn=lambda data: (
            data.get("status", {}).get("connectedServer") or {}
        ),
    ),
    MularrSensorEntityDescription(
        key="active_downloads",
        translation_key="active_downloads",
        name="Active Downloads",
        icon="mdi:download-multiple",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: (
            data.get("speed", {}).get("sample", {}).get("activeAmule")
            if data.get("speed", {}).get("sample")
            else len(data.get("transfers", {}).get("list", []))
        ),
    ),
    MularrSensorEntityDescription(
        key="shared_files",
        translation_key="shared_files",
        name="Shared Files",
        icon="mdi:folder-upload",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("status", {}).get("sharedFileCount", 0),
    ),
    MularrSensorEntityDescription(
        key="total_sources",
        translation_key="total_sources",
        name="Total Sources",
        icon="mdi:account-group",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("status", {}).get("totalSourceCount", 0),
    ),
    MularrSensorEntityDescription(
        key="upload_queue",
        translation_key="upload_queue",
        name="Upload Queue",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("status", {}).get("uploadQueueLength", 0),
    ),
    MularrSensorEntityDescription(
        key="total_downloaded",
        translation_key="total_downloaded",
        name="Total Downloaded",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.get("status", {}).get("totalReceivedBytes"),
    ),
    MularrSensorEntityDescription(
        key="total_uploaded",
        translation_key="total_uploaded",
        name="Total Uploaded",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.get("status", {}).get("totalSentBytes"),
    ),
    MularrSensorEntityDescription(
        key="free_disk_space",
        translation_key="free_disk_space",
        name="Free Disk Space",
        icon="mdi:harddisk",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        value_fn=lambda data: (
            data.get("system", {}).get("disks", [{}])[0].get("free")
            if data.get("system", {}).get("disks")
            else None
        ),
    ),
    MularrSensorEntityDescription(
        key="public_ip",
        translation_key="public_ip",
        name="Public IP",
        icon="mdi:ip",
        value_fn=lambda data: data.get("system", {}).get("publicIp"),
        attrs_fn=lambda data: (
            data.get("system", {}).get("ipDetails")
            if isinstance(data.get("system", {}).get("ipDetails"), dict)
            else {}
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Mularr sensor platform."""
    coordinator: MularrDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        MularrSensor(coordinator, entry.entry_id, description)
        for description in SENSOR_TYPES
    )


class MularrSensor(MularrEntity, SensorEntity):
    """Representation of a Mularr sensor."""

    entity_description: MularrSensorEntityDescription

    def __init__(
        self,
        coordinator: MularrDataUpdateCoordinator,
        entry_id: str,
        description: MularrSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry_id, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the extra state attributes."""
        if self.entity_description.attrs_fn:
            return self.entity_description.attrs_fn(self.coordinator.data)
        return {}
