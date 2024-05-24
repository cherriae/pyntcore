from __future__ import annotations

import logging
from typing import Dict, Iterator, List, Any, Callable

from ntcore.enums import NetworkTablesType

logging.basicConfig(level=logging.DEBUG)

class Topic:
    """
    Represents a topic in NTCore with methods to subscribe, publish, set value, and publish value. 
    Includes functionality to handle subscribers and publishing values
    """
    def __init__(self, ntcore, name: str, type_info: NetworkTablesType, default_value: Any):
        self.ntcore = ntcore
        self.name: str = name
        self.type_info: NetworkTablesType = type_info
        self.default_value: Any = default_value
        self.subscribers: List[Callable[[Any], None]] = []
        self.publisher: bool = False

    def __repr__(self):
        return f"Topic(name='{self.name}', type='{self.type_info.name}', default_value={self.default_value}, publisher={self.publisher})"

    def __str__(self):
        return f"Topic '{self.name}' (type: {self.type_info.name}, default value: {self.default_value})"
    
    def __iter__(self) -> Iterator[Callable[[Any], None]]:
        self._iterator_index = 0  # Reset the iterator index
        return self

    def __next__(self) -> Callable[[Any], None]:
        if self._iterator_index >= len(self.subscribers):
            raise StopIteration
        subscriber = self.subscribers[self._iterator_index]
        self._iterator_index += 1
        return subscriber

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
        logging.debug(f"Subscribed callback {callback} to topic {self.name}")

    def unsubscribe(self, callback: Callable[[Any], None]):
        """
        Unsubscribe a callback from the topic.
        Removes a callback function from the list of subscribers for the topic.

        Args:
        - callback: Callable[[Any], None]

        Returns: None
        """
        self.subscribers.remove(callback)
        logging.debug(f"Unsubscribed callback {callback} from topic {self.name}")

    def publish(self, properties: Dict[str, Any] = None):
        """
        Set a value for the topic.

        Args:
        - properties: Dict[str, Any]

    
        Returns: None
        """
        self.publisher = True
        if self.default_value is not None:
            self.publish_value(self.default_value)
        logging.info(f"Published topic {self.name}")

    def unpublish(self):
        """
        Unpublish the topic.
        Sets the publisher flag to False and clears the list of subscribers.

        Returns: None
        """
        self.publisher = False
        self.subscribers.clear()
        logging.info(f"Unpublished topic {self.name}")

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
            logging.debug(f"Set value {value} for topic {self.name}")
        else:
            raise ValueError("This topic is not published")

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
        self.ntcore.send(message)
        for callback in self.subscribers:
            callback(value)
        logging.debug(f"Published value {value} to topic {self.name}")
