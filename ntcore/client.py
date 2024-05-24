import socket
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
    def __init__(self):
        self.topics: Dict[str, Topic] = {}
        self.socket: socket.socket = None

    def get_instance_by_team(self, team_address: str, port: int):
        """
        Get an instance of NTCore by team address.

        Args:
            team_address: str
            port: int

        Returns:
            Instance of NTCore
        """
        self._connect(team_address, port)
        return self

    def _connect(self, address: str, port: int):
        """
        Establish a socket connection to the specified address and port.

        Args:
        - address: str
        - port: int

        Returns: None
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((address, port))
            logging.info(f"Connected to {address}:{port}")
        except Exception as e:
            logging.error(f"Failed to connect to {address}:{port} - {e}")
            raise

    def create_topic(self, name: str, type_info: NetworkTablesType, default_value: Any = None) -> Topic:
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
        logging.info(f"Created topic: {name}")
        return topic

    def send(self, message: Dict[str, Any]):
        """
        Send a message through the socket.

        Args:
        - message: Dict[str, Any]

        Returns: None
        """
        try:
            self.socket.sendall(json.dumps(message).encode('utf-8'))
            logging.debug(f"Sent message: {message}")
        except Exception as e:
            logging.error(f"Failed to send message - {e}")
            raise

    def publish_value(self, value: Any):
        """
        Publish a value to the subscribers of the topic.

        Args:
        - value: Any

        Returns: None
        """
        message = {
            'name': self.name,
            'type': self.type_info.value,
            'value': value
        }
        self.send(message)
        for callback in self.subscribers:
            callback(value)

    def __repr__(self):
        return f"NTCore(topics={list(self.topics.keys())})"

    def __str__(self):
        return "NTCore instance"

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
