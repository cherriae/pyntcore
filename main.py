from __future__ import annotations

from typing import Union
from ntcore.client import NTCore
from ntcore.enums import NetworkTablesType

import asyncio


# Create the autoMode topic w/ a default return value of 'No Auto'
async def e():
    team_address: Union[None, str] = "localhost:5810" # if simulation
    ntcore_instance = await NTCore.get_instance_by_team(team_address)
    global auto_mode_topic
    auto_mode_topic = await ntcore_instance.create_topic('/MyTable/autoMode', NetworkTablesType.STRING, 'No Auto')

asyncio.run(e())

# Publish the topic
auto_mode_topic.publish()

# Set a new value
auto_mode_topic.set_value('25 Ball Auto and Climb')

# Testing values
print(auto_mode_topic)
print(str(auto_mode_topic))
print(repr(auto_mode_topic))
print(list(auto_mode_topic))