
import datetime
import uuid


class Utils:
    def __init__(self) -> None:
        self.used_ids = []
        
        self.uri: str
        self.port: int

    def generateUid(self) -> int: 
        uid_str = str(uuid.uuid4())
        id_num = sum(ord(char) for char in uid_str)
        uid = id_num + int(datetime.now().timestamp() * 1000)

        if uid in self.used_ids:
            return self.generateUid()

        self.used_ids.append(uid)
        return uid
    
    @staticmethod
    def getRobotAddress(team: int) -> str:
        return f"roborio-{team}-frc.local"
    
    def createServerUrl(self, uri: str, port: int) -> str:
        self.uri = uri
        self.port = port
        return f"ws://{uri}:{port}/nt/ntcore-py-{self.generateUid()}"

    @property
    def uri(self):
        return self.uri
    
    @property
    def port(self):
        return self.port