from typing import Any
from Token import Token

class Msg:
    def __init__(self, payload: Any, stamp: int) -> None:
        self.payload = payload
        self.stamp = stamp
    
    def getPayload(self):
        return self.payload

class Msg4Send(Msg):
    def __init__(self, payload: Any, stamp:int, toId :int,) -> None:
        super().__init__(payload, stamp)
        self.toId = toId

class Msg4Broadcast(Msg):
    def __init__(self, payload:Any, stamp:int, fromId:int) -> None:
        super().__init__(payload, stamp)
        self.fromId = fromId

class Msg4TokenTransfere(Msg):
    def __init__(self, payload:Token, stamp:int) -> None:
        super().__init__(payload, stamp)


# region init msgs

class Msg4Ready(Msg):
    def __init__(self, payload:None, stamp:int) -> None:
        super().__init__(payload, stamp)


class Msg4AllReady(Msg):
    def __init__(self, payload:None, stamp:int) -> None:
        super().__init__(payload, stamp)


class Msg4IdConsensus(Msg):
    def __init__(self, payload:None, stamp:int, preId :int) -> None:
        super().__init__(payload, stamp)
        self.preId = preId

# endregion init msgs