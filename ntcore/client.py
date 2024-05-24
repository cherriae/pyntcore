import asyncio

from ntcore import logger
from ntcore.entry import NetworkTableEntry

class NetworkTablesProtocol:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.reader = None
        self.writer = None
        self.entries = {}

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.server_address, self.server_port)
        logger.info(f"Connected to {self.server_address}:{self.server_port}")

    def disconnect(self):
        if self.writer:
            self.writer.close()
            logger.info("Disconnected from server")

    async def send_data(self, data):
        if self.writer:
            self.writer.write(data)
            await self.writer.drain()

    async def receive_data(self):
        if self.reader:
            return await self.reader.read(1024)

    def handle_entry_update(self, entry_name, entry_type, value):
        if entry_name in self.entries:
            entry = self.entries[entry_name]
            entry.setValue(value)
        else:
            entry = NetworkTableEntry(entry_name, entry_type, value)
            self.entries[entry_name] = entry

    def __repr__(self):
        return f"NetworkTablesProtocol(server_address={self.server_address}, server_port={self.server_port})"

    def __str__(self):
        return f"NetworkTablesProtocol connected to {self.server_address}:{self.server_port}"

    def __list__(self):
        return list(self.entries.keys())
