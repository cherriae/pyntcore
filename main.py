from __future__ import annotations
import asyncio

from ntcore.core import NTCore, NetworkTablesType

class Client(NTCore):

    def __init__(self):
        super().__init__()

    async def run(self) -> Client:
        self.ntcore_instance = await self.get_instance_by_team("localhost", 5810)
        return self

    async def topic(self) -> None:  # path: str, networkTableType: NetworkTablesType, name: str

        # Add topics
        auto_mode_topic = self.ntcore_instance.create_topic(name='/SmartDashboard/autoMode', default_value=b'No Auto')
        auto = self.ntcore_instance.create_topic(name='/SmartDashboard/Autoe', default_value=b'Auto')

        print(repr(auto_mode_topic))

        await self._print(auto)

        auto_mode_topic.setValue('25 Ball Auto and Climb')


        await self._print(auto_mode_topic)

    async def _print(self, topic) -> None:
        print(topic)
        print(repr(topic))



if __name__ == "__main__":
    client = Client()
    asyncio.run(client.run())
    asyncio.run(client.topic())
