"""DataUpdateCoordinator for Mularr integration."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .mularr_api import MularrApiClient, MularrApiError, MularrConnectionError, MularrAuthError

_LOGGER = logging.getLogger(__name__)


class MularrDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Mularr data from API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: MularrApiClient,
        update_interval: int = DEFAULT_SCAN_INTERVAL,
        version: str | None = None,
    ) -> None:
        """Initialize the coordinator."""
        self.client = client
        self.version = version
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Mularr API."""
        try:
            return await self.client.get_all_data()
        except MularrAuthError as err:
            raise UpdateFailed(f"Authentication failed: {err}") from err
        except (MularrConnectionError, MularrApiError) as err:
            raise UpdateFailed(f"Error communicating with Mularr API: {err}") from err
