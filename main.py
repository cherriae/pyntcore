from __future__ import annotations

from ntcore import Topic, NTCore, NetworkTablesType

class Client(NTCore):
    def __init__(self):
        super().__init__()

    def run(self) -> Client:
        self.ntcore_instance = self.get_instance_by_team("localhost", 5810)
        return self

    def topic(self) -> None: #path: str, networkTableType: NetworkTablesType, name: str
        # Add topics
        auto_mode_topic = self.ntcore_instance.create_topic('/MyTable/autoMode', NetworkTablesType.STRING, 'No Auto')
        auto = self.ntcore_instance.create_topic('/MyTable/Auto', NetworkTablesType.STRING, 'Auto')    

        auto_mode_topic.publish()
        auto.publish()

        # print(auto_mode_topic)
        # print(repr(auto_mode_topic))
        # self._print(auto)

        # auto_mode_topic.set_value('25 Ball Auto and Climb')
        # TODO: fix set_value

        # self._print(auto_mode_topic)

    def _print(self, topic) -> None:
        print(topic)
        print(repr(topic))
        print(list(self.ntcore_instance))

if __name__ == "__main__":
    e = Client()
    e.run()
    e.topic()