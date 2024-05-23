from __future__ import annotations

import socket
import asyncio
import json
import logging
from typing import Dict, Any, Iterator

from ntcore.enums import NetworkTablesType
from ntcore.topic import Topic

logging.basicConfig(level=logging.DEBUG)



class NTCore:
    """
    Class representing the core functionality of NTCore.
    """
    def __init__(self, team_address: str):
        self.topics: Dict[str, Topic] = {}
        self.socket: socket.socket = None

        self._team_address: str = team_address or f"roborio-{973}-frc.local"

    def __repr__(self):
        return f"NTCore(team_address='{self._team_address}', topics={list(self.topics.keys())})"

    def __str__(self):
        return f"NTCore instance for team {self._team_address.split('-')[1]}"

    def __iter__(self) -> Iterator[Topic]:
        self._iterator_index = 0  # Reset the iterator index
        return self

    def __next__(self) -> Topic:
        topics_list = list(self.topics.values())
        if self._iterator_index >= len(topics_list):
            raise StopIteration
        topic = topics_list[self._iterator_index]
        self._iterator_index += 1
        return topic

    @classmethod
    async def get_instance_by_team(cls, arg1, arg2=None):
        """
        Get an instance of NTCore by team address.

        Args:
            arg1: str (team_address) if arg2 is provided, else str (team_address:port)
            arg2: int, optional (port)

        Returns:
            Instance of NTCore
        """
        if arg2 is None:
            team_address, port = arg1.split(':')
            port = int(port)
        else:
            team_address = arg1
            port = arg2

        instance = cls(team_address)
        await instance._connect(team_address or instance._team_address, port)
        return instance

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
