import asyncio
from functools import partial

import voluptuous as vol
import logging
#import pandas as pd
from homeassistant import config_entries, core
from datetime import datetime
import sys
from datetime import timedelta
from typing import Any, Callable, Dict, Optional
import homeassistant.helpers.config_validation as cv
from homeassistant.components.text import TextEntity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
from .const import (
DOMAIN
)

_LOGGER = logging.getLogger(__name__)



async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]

    entity_id = config["entity_id"]
    num_codes = config["num_codes"]

    sensors = []
    for index in range(0, num_codes):
        sensors[index] = LockManagerCode(hass, entity_id, index)

    async_add_entities(sensors, update_before_add=True)

    # def log_to_gspread(call):

    #hass.services.async_register(DOMAIN, "log", log_to_gspread)


class LockManagerCode(TextEntity):
    """Representation of a Lock Manager Code."""

    def __init__(self, hass: HomeAssistantType, entity_id: str, code_index: int):
        super().__init__()
        self._lock_entity_id = entity_id
        self._code_index = code_index
        self.hass = hass
        self._name = "Code " + code_index
        self._available = True
        self._state = ""

        self._attrs: Dict[str, Any] = {}

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._lock_entity_id + "_code_" + self._code_index

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> Optional[str]:
        return self._state

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self._attrs

    async def async_set_value(self, value: str):
        self._state = value