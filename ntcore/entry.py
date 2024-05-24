from typing import Any, Callable
from ntcore import logger

class NetworkTableEntry:
    def __init__(self, name, entry_type, value=None):
        self.name = name
        self.entry_type = entry_type
        self.value = value
        self.callbacks = []

    def setValue(self, value):
        self.value = value
        self._notify_callbacks(value)
        logger.debug(f"Set `{self.name}` Value From: `{self.value}` To: `{value}`")

    def getValue(self):
        return self.value

    def addListener(self, callback: Callable[[Any], None]):
        logger.info(f"Added Listener To: {self.name}")
        self.callbacks.append(callback)

    async def async_setValue(self, value):
        self.setValue(value)

    async def async_getValue(self):
        return self.getValue()

    def _notify_callbacks(self, value):
        logger.debug(f"Notify Callback: {value}")
        for callback in self.callbacks:
            callback(value)

    def __repr__(self):
        return f"NetworkTableEntry(name={self.name}, entry_type={self.entry_type}, value={self.value})"

    def __str__(self):
        return f"NetworkTableEntry '{self.name}' of type {self.entry_type} with value: {self.value}"

    def __list__(self):
        return [self.name, self.entry_type, self.value]
