from __future__ import annotations

import logging
from typing import Dict, List, Any, Callable

from ntcore.enums import NetworkTablesType
from ntcore.ntcore import NTCore

logging.basicConfig(level=logging.DEBUG)


class Topic:
    """
    Represents a topic in NTCore with methods to subscribe, publish, set value, and publish value. 
    Includes functionality to handle subscribers and publishing values asynchronously.
    """
    def __init__(self, ntcore: NTCore, name: str, type_info: NetworkTablesType, default_value: Any):
        self.ntcore: NTCore = ntcore
        self.name: str = name
        self.type_info: NetworkTablesType = type_info
        self.default_value: Any = default_value
        self.subscribers: List[Callable[[Any], None]] = []
        self.publisher: bool = False

        if default_value is not None:
            self.publish_value(default_value)

    def subscribe(self, callback: Callable[[Any], None], immediate_notify: bool = False):
        """
        Subscribe a callback to the topic.

        Adds a callback function to the list of subscribers for the topic. 
        If immediate_notify is True and a default value is set, the callback is immediately triggered with the default value.

        Args:
        - callback: Callable[[Any], None]
        - immediate_notify: bool, optional

        Returns: None
        """
        self.subscribers.append(callback)
        if immediate_notify and self.default_value is not None:
            callback(self.default_value)

    def publish(self, properties: Dict[str, Any] = None):
        """
        Set a value for the topic.

        Args:
        - value: Any

        Raises:
        - ValueError: If trying to set value on an unpublished topic

        Returns: None
        """
        self.publisher = True
        if self.default_value is not None:
            self.publish_value(self.default_value)

    def set_value(self, value: Any):
        """
        Publish a value for the topic.

        Args:
        - value: Any

        Raises:
        - ValueError: If trying to publish value on an unpublished topic

        Returns: None
        """

        if self.publisher:
            self.publish_value(value)
        else:
            raise ValueError("This topic is not published")

    async def publish_value(self, value: Any):
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
        await self.ntcore.send(message)
        for callback in self.subscribers:
            callback(value)
