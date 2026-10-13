"""Asynchronous API client for Mularr."""
from __future__ import annotations

import asyncio
import logging
from typing import Any
import aiohttp

_LOGGER = logging.getLogger(__name__)


class MularrApiError(Exception):
    """Base exception for Mularr API errors."""


class MularrAuthError(MularrApiError):
    """Exception for authentication errors."""


class MularrConnectionError(MularrApiError):
    """Exception for connection errors."""


class MularrApiClient:
    """Client for Mularr REST API."""

    def __init__(
        self,
        host: str,
        port: int = 8940,
        api_key: str | None = None,
        use_ssl: bool = False,
        verify_ssl: bool = True,
        session: aiohttp.ClientSession | None = None,
        timeout: int = 10,
    ) -> None:
        """Initialize the client."""
        self.host = host.strip().rstrip("/")
        if self.host.startswith("http://") or self.host.startswith("https://"):
            scheme, netloc = self.host.split("://", 1)
            use_ssl = scheme == "https"
            self.host = netloc

        self.port = port
        self.api_key = api_key
        self.use_ssl = use_ssl
        self.verify_ssl = verify_ssl
        self._session = session
        self._timeout = aiohttp.ClientTimeout(total=timeout)

        protocol = "https" if self.use_ssl else "http"
        self.base_url = f"{protocol}://{self.host}:{self.port}"

    def _get_headers(self) -> dict[str, str]:
        """Build request headers."""
        headers = {"Content-Type": "application/json"}
        if self.api_key and self.api_key.strip():
            headers["X-Api-Key"] = self.api_key.strip()
        return headers

    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
    ) -> Any:
        """Execute HTTP request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        close_session = False
        session = self._session
        if session is None or session.closed:
            connector = aiohttp.TCPConnector(ssl=self.verify_ssl if self.use_ssl else None)
            session = aiohttp.ClientSession(connector=connector, timeout=self._timeout)
            close_session = True

        try:
            async with session.request(
                method,
                url,
                headers=headers,
                json=json_data,
            ) as response:
                if response.status in (401, 403):
                    text = await response.text()
                    raise MularrAuthError(f"Authentication failed: {text}")

                if response.status >= 400:
                    text = await response.text()
                    raise MularrApiError(f"HTTP {response.status}: {text}")

                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return await response.json()
                return await response.text()

        except asyncio.TimeoutError as err:
            raise MularrConnectionError(f"Timeout connecting to Mularr: {err}") from err
        except aiohttp.ClientError as err:
            raise MularrConnectionError(f"Error connecting to Mularr: {err}") from err
        finally:
            if close_session and session and not session.closed:
                await session.close()

    async def test_connection(self) -> bool:
        """Test connection and authentication."""
        try:
            await self._request("GET", "/api/amule/status")
            return True
        except (MularrApiError, MularrConnectionError):
            raise

    async def get_status(self) -> dict[str, Any]:
        """Fetch aMule status."""
        return await self._request("GET", "/api/amule/status")

    async def get_speed_latest(self) -> dict[str, Any]:
        """Fetch latest speed statistics."""
        return await self._request("GET", "/api/stats/speed-latest")

    async def get_system_info(self) -> dict[str, Any]:
        """Fetch system and VPN info."""
        return await self._request("GET", "/api/system/info")

    async def get_transfers(self) -> dict[str, Any]:
        """Fetch active transfers list."""
        return await self._request("GET", "/api/amule/transfers")

    async def get_all_data(self) -> dict[str, Any]:
        """Fetch all data simultaneously."""
        status, speed, system, transfers = await asyncio.gather(
            self.get_status(),
            self.get_speed_latest(),
            self.get_system_info(),
            self.get_transfers(),
            return_exceptions=True,
        )

        result: dict[str, Any] = {}
        if isinstance(status, dict):
            result["status"] = status
        elif isinstance(status, Exception):
            _LOGGER.debug("Error fetching status: %s", status)
            result["status"] = {}

        if isinstance(speed, dict):
            result["speed"] = speed
        elif isinstance(speed, Exception):
            _LOGGER.debug("Error fetching speed: %s", speed)
            result["speed"] = {}

        if isinstance(system, dict):
            result["system"] = system
        elif isinstance(system, Exception):
            _LOGGER.debug("Error fetching system info: %s", system)
            result["system"] = {}

        if isinstance(transfers, dict):
            result["transfers"] = transfers
        elif isinstance(transfers, Exception):
            _LOGGER.debug("Error fetching transfers: %s", transfers)
            result["transfers"] = {}

        # If all requests failed with errors, raise error
        if not any(result.values()):
            raise MularrConnectionError("Failed to fetch any data from Mularr")

        return result

    async def restart_daemon(self) -> bool:
        """Restart aMule daemon."""
        await self._request("POST", "/api/amule/daemon/restart")
        return True

    async def connect_server(self) -> bool:
        """Connect to ED2K server."""
        await self._request("POST", "/api/amule/server/connect")
        return True

    async def disconnect_server(self) -> bool:
        """Disconnect from ED2K server."""
        await self._request("POST", "/api/amule/server/disconnect")
        return True

    async def clear_completed(self) -> bool:
        """Clear completed downloads."""
        await self._request("POST", "/api/amule/transfers/clear-completed")
        return True
