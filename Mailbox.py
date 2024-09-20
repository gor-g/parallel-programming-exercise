from collections import deque
from Msg import Msg

class Mailbox:
    def __init__(self):
        self.msgQue = deque()

    def isEmpty(self) -> bool:
        return len(self.msgQue) == 0

    def addMessage(self, msg: Msg):
        self.msgQue.append(msg)

    def getMessage(self) -> Msg:
        m = self.msgQue.popleft()
        print(m)
        return m
