import json
from typing import Any, Callable
import asyncio

from ntcore.client import NetworkTablesProtocol
from ntcore.entry import NetworkTableEntry
from ntcore import logger

class NetworkTablesType:
    BOOLEAN = 0
    NUMBER = 1
    STRING = 2
    RAW = 3

    @classmethod
    def from_value(cls, value):
        if isinstance(value, bool):
            return cls.BOOLEAN
        elif isinstance(value, (int, float)):
            return cls.NUMBER
        elif isinstance(value, str):
            return cls.STRING
        else:
            return cls.RAW


class NTCore:
    def __init__(self):
        self.protocol = None

    async def get_instance_by_team(self, team_address, port=1735):
        self.protocol = NetworkTablesProtocol(team_address, port)
        await self.protocol.connect()
        return self

    def create_topic(self, name: str, default_value=None):
        if self.protocol is None:
            raise ValueError("Instance not initialized. Call get_instance_by_team first.")
            
        entry_type = NetworkTablesType.from_value(default_value)

        entry = NetworkTableEntry(name, entry_type, default_value)
        self.protocol.entries[name] = entry
        logger.info(f"Created topic: {name}: {default_value}")
        return entry

    async def send(self, name, value):
        if name not in self.protocol.entries:
            raise ValueError(f"Topic {name} does not exist.")

        entry = self.protocol.entries[name]
        entry_type = entry.entry_type
        data = self._serialize_entry(name, entry_type, value)
        await self.protocol.send_data(data)
        logger.debug(f"Sent value {value} to topic {name}")

    def subscribe(self, name, callback: Callable[[Any], None]):
        if name not in self.protocol.entries:
            raise ValueError(f"Topic {name} does not exist.")

        entry = self.protocol.entries[name]
        entry.addListener(callback)
        logger.info(f"Subscribed to topic: {name}")

    def _serialize_entry(self, name, entry_type, value):
        data = {
            "name": name,
            "type": entry_type.value,
            "value": value
        }
        return json.dumps(data).encode()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.protocol:
            await self.protocol.disconnect()

    def __repr__(self):
        return f"NTCore(protocol={self.protocol})"

    def __str__(self):
        return f"NTCore instance with protocol: {self.protocol}"

    def __list__(self):
        return list(self.protocol.entries.keys()) if self.protocol else []
