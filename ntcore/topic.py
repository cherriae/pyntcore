from __future__ import annotations

import logging
from typing import Dict, List, Any, Callable

from ntcore.enums import NetworkTablesType
from ntcore.ntcore import NTCore

logging.basicConfig(level=logging.DEBUG)


class Topic:
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
        self.subscribers.append(callback)
        if immediate_notify and self.default_value is not None:
            callback(self.default_value)

    def publish(self, properties: Dict[str, Any] = None):
        self.publisher = True
        if self.default_value is not None:
            self.publish_value(self.default_value)

    def set_value(self, value: Any):
        if self.publisher:
            self.publish_value(value)
        else:
            raise ValueError("This topic is not published")

    async def publish_value(self, value: Any):
        message = {
            'name': self.name,
            'type': self.type_info.value,
            'value': value
        }
        await self.ntcore.send(message)
        for callback in self.subscribers:
            callback(value)
