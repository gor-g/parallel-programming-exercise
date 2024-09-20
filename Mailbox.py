from collections import deque
from Msg import Msg

class Mailbox:
    def __init__(self):
        self.msgQue = deque()

    def isEmpty(self) -> bool:
        return len(self.msgQue) == 0

    def addMessage(self, msg: Msg):
        self.msgQue.append(msg)

    def getMsg(self) -> Msg:
        return self.msgQue.popleft()
