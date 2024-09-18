from typing import Any

class MessageForSend():
  def __init__(self, payload: Any, recieverId :int, timestamp:int) -> None:
    self.payload = payload
    self.recieverId = recieverId
    self.timestamp = timestamp

  def getPayload(self):
    return self.payload

    