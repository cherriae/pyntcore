from __future__ import annotations

import socket
import asyncio
import json
import logging
from typing import Dict, Any

from ntcore.enums import NetworkTablesType
from ntcore.topic import Topic

logging.basicConfig(level=logging.DEBUG)



class NTCore:
    def __init__(self, team_id: int):
        self.topics: Dict[str, Topic] = {}
        self.socket: socket.socket = None

        self._team_address: str = f"roborio-{team_id}-frc.local"

    async def get_instance_by_team(self, team_address: str = None, port: int = 5810):
        return await self._connect(team_address or self._team_address, port)

    async def _connect(self, address: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await asyncio.get_event_loop().sock_connect(self.socket, (address, port))
        return self

    def create_topic(self, name: str, type_info: NetworkTablesType, default_value: Any = None) -> 'Topic':
        topic = Topic(self, name, type_info, default_value)
        self.topics[name] = topic
        return topic

    async def send(self, message: Dict[str, Any]):
        await asyncio.get_event_loop().sock_sendall(self.socket, json.dumps(message).encode('utf-8'))
