"""Config flow for Mularr integration."""
from __future__ import annotations

import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

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
)
from .mularr_api import (
    MularrApiClient,
    MularrAuthError,
    MularrConnectionError,
)

_LOGGER = logging.getLogger(__name__)


class MularrConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Mularr."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            api_key = user_input.get(CONF_API_KEY)
            use_ssl = user_input.get(CONF_SSL, DEFAULT_SSL)

            unique_id = f"{host}:{port}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            client = MularrApiClient(
                host=host,
                port=port,
                api_key=api_key,
                use_ssl=use_ssl,
                session=session,
            )

            try:
                await client.test_connection()
            except MularrAuthError:
                errors["base"] = "invalid_auth"
            except MularrConnectionError:
                errors["base"] = "cannot_connect"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception connecting to Mularr: %s", err)
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=f"Mularr ({host})",
                    data=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default="192.168.60.2"): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Optional(CONF_API_KEY): str,
                vol.Optional(CONF_SSL, default=DEFAULT_SSL): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get options flow."""
        return MularrOptionsFlowHandler(config_entry)


class MularrOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Mularr options."""

    def __init__(self, config_entry: config_entries.ConfigEntry | None = None) -> None:
        """Initialize options flow."""
        self._config_entry_compat = config_entry

    @property
    def config_entry(self) -> config_entries.ConfigEntry:
        """Return current config entry in a backwards-compatible manner."""
        try:
            entry = super().config_entry
            if entry is not None:
                return entry
        except Exception:
            pass
        return self._config_entry_compat

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage connection options and update interval."""
        errors: dict[str, str] = {}
        entry = self.config_entry

        current_host = entry.options.get(CONF_HOST, entry.data.get(CONF_HOST, "192.168.60.2"))
        current_port = entry.options.get(CONF_PORT, entry.data.get(CONF_PORT, DEFAULT_PORT))
        current_api_key = entry.options.get(CONF_API_KEY, entry.data.get(CONF_API_KEY, ""))
        current_ssl = entry.options.get(CONF_SSL, entry.data.get(CONF_SSL, DEFAULT_SSL))
        current_scan = entry.options.get(
            CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            api_key = user_input.get(CONF_API_KEY)
            use_ssl = user_input.get(CONF_SSL, DEFAULT_SSL)

            session = async_get_clientsession(self.hass)
            client = MularrApiClient(
                host=host,
                port=port,
                api_key=api_key,
                use_ssl=use_ssl,
                session=session,
            )

            try:
                await client.test_connection()
            except MularrAuthError:
                errors["base"] = "invalid_auth"
            except MularrConnectionError:
                errors["base"] = "cannot_connect"
            except Exception as err:
                _LOGGER.exception("Unexpected exception connecting to Mularr: %s", err)
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=current_host): str,
                vol.Required(CONF_PORT, default=current_port): int,
                vol.Optional(CONF_API_KEY, default=current_api_key if current_api_key else ""): str,
                vol.Optional(CONF_SSL, default=current_ssl): bool,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=current_scan,
                ): vol.All(vol.Coerce(int), vol.Range(min=2, max=300)),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )
