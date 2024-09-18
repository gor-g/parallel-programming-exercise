from time import sleep
from typing import Any
from pyeventbus3.pyeventbus3 import PyBus, subscribe, Mode
from MessageForSend import MessageForSend
from BroadcastMessage import BroadcastMessage
from Token import Token

class Com():
    nbProcessCreated = 0

    def __init__(self):
        self.myId = Com.nbProcessCreated
        Com.nbProcessCreated += 1
        PyBus.Instance().register(self, self)
        self.lamportClock = 0
        self.token = None
        self.alive = True

    def getNbProcess(self):
        return Com.nbProcessCreated

    def getMyId(self):
        return self.myId

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageForSend)
    def onRecieve(self, event: MessageForSend):
        if event.recieverId == self.myId:
            self.lamportClock = max(self.lamportClock, event.timestamp) + 1

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event: BroadcastMessage):
        if event.senderId != self.myId:
            self.lamportClock = max(self.lamportClock, event.timestamp) + 1

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Token)
    def onToken(self, event: Token):
        if event.holderId == self.myId:
            self.token = event
            self.manageToken()

    def sendTo(self, msg: Any, recieverId: int):
        self.post(
            MessageForSend(msg,
                           recieverId,
                           self.lamportClock)
        )

    def broadcast(self, msg: Any):
        self.post(
            BroadcastMessage(msg,
                             self.lamportClock,
                             senderId=self.myId)
        )

    def manageToken(self):
        while self.token:
            sleep(0.01)
            if not self.token.isInUse:
                self.transfereToken()

    def requestSc(self):
        while not self.token:
            sleep(0.01)
        self.token.use()

    def releaseSc(self):
        self.token.release()

    def transfereToken(self):
        self.post(
            self.token.changeHolder(
                self.nextId()
            )
        )
        self.token = None

    def launchToken(self):
        self.post(Token(self.myId))

    def post(self, obj: Any):
        self.lamportClock += 1
        PyBus.Instance().post(obj)

    def nextId(self):
        return (self.myId + 1) % Com.nbProcessCreated


    def stop(self):
        self.alive = False

