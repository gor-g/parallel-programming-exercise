from typing import Any
from Token import Token

class Msg:
    def __init__(self, payload: Any) -> None:
        self.payload = payload
        self.stamp : int | None= None
    
    def getPayload(self):
        return self.payload
    
    def setStamp(self, stamp):
        self.stamp = stamp

class Msg4Send(Msg):
    def __init__(self, payload: Any, toId :int,) -> None:
        super().__init__(payload)
        self.toId = toId

class Msg4Broadcast(Msg):
    def __init__(self, payload:Any, fromId:int) -> None:
        super().__init__(payload)
        self.fromId = fromId

class Msg4TokenTransfere(Msg):
    def __init__(self, payload:Token) -> None:
        super().__init__(payload)

# region init msgs

class Msg4Ready(Msg):
    def __init__(self, payload:None) -> None:
        super().__init__(payload)


class Msg4AllReady(Msg):
    def __init__(self, payload:None) -> None:
        super().__init__(payload)


class Msg4IdConsensus(Msg):
    def __init__(self, payload:int) -> None:
        super().__init__(payload)

# endregion init msgs