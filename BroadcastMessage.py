from typing import Any


class BroadcastMessage:
  def __init__(self, payload:Any, timestamp:int, senderId:int) -> None:
    self.payload = payload
    self.timestamp = timestamp
    self.senderId = senderId

  def getPayload(self):
    return self.payload