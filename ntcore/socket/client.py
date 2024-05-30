from __future__ import annotations

from ..types import BinaryMessageData
from typing import Any, Dict, List
import websocket
import pickle


class NetworkTables:
    def __init__(self, server_url: str) -> None:
        self.server_url = server_url
        self.websocket = websocket.create_connection(server_url)
        self.entries: Dict[int, Any] = {}

    def putValue(self, key: str, value: Any) -> None:
        type_info = NetworkTablesTypeInfo.get_network_tables_type_from_object(value)
        topic_id = self._get_or_create_topic_id(key)
        binary_data = self._encode_binary_data(topic_id, type_info, value)
        self.websocket.send(binary_data)

    def getValue(self, key: str) -> Any:
        topic_id = self._get_or_create_topic_id(key)
        return self.entries.get(topic_id, None)

    def _get_or_create_topic_id(self, key: str) -> int:
        if key not in self.entries:
            self.entries[key] = len(self.entries)
        return self.entries[key]

    def _encode_binary_data(self, topic_id: int, type_info: List[int, str], value: Any) -> bytes:
        binary_data = BinaryMessageData(
            topicId=topic_id,
            serverTime=int(time.time() * 1000),
            typeInfo=type_info,
            value=value
        )
        return pickle.dumps(binary_data)

    def _decode_binary_data(self, binary_data: bytes) -> BinaryMessageData:
        return pickle.loads(binary_data)

    def run(self) -> None:
        while True:
            binary_data = self.websocket.recv()
            binary_message_data = self._decode_binary_data(binary_data)
            self.entries[binary_message_data.topicId] = binary_message_data.value