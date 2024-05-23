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
    """
    Class representing the core functionality of NTCore.
    """
    def __init__(self, team_id: int):
        self.topics: Dict[str, Topic] = {}
        self.socket: socket.socket = None

        self._team_address: str = f"roborio-{team_id}-frc.local"

    async def get_instance_by_team(self, team_address: str = None, port: int = 5810):
        """
        Get an instance of NTCore by team address.

        Args:
        - team_address: str, optional
        - port: int

        Returns: Instance of NTCore
        """

        return await self._connect(team_address or self._team_address, port)

    async def _connect(self, address: str, port: int):
        """
        Establish a socket connection to the specified address and port.

        Args:
        - address: str
        - port: int

        Returns: Instance of NTCore
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await asyncio.get_event_loop().sock_connect(self.socket, (address, port))
        return self

    def create_topic(self, name: str, type_info: NetworkTablesType, default_value: Any = None) -> 'Topic':
        """
        Create a topic and add it to the topics dictionary.

        Args:
        - name: str
        - type_info: NetworkTablesType
        - default_value: Any

        Returns: Instance of Topic
        """

        topic = Topic(self, name, type_info, default_value)
        self.topics[name] = topic
        return topic

    async def send(self, message: Dict[str, Any]):
        """
        Send a message through the socket.

        Args:
        - message: Dict[str, Any]

        Returns: None
        """

        await asyncio.get_event_loop().sock_sendall(self.socket, json.dumps(message).encode('utf-8'))
