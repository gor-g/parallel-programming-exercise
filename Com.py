from time import sleep
from typing import Any
import random
from pyeventbus3.pyeventbus3 import PyBus, subscribe, Mode
from Token import Token
from Msg import *

class Com():

    def __init__(self, nbProcess):
        self.myId = None
        self.nbProcess = nbProcess
        PyBus.Instance().register(self, self)
        self.clock = 0
        self.alive = True
        self.token = None

        self._countReady = 1
        self._allReady = False




    def getNbProcess(self):
        return self.nbProcess

    def getMyId(self):
        return self.myId

    # region Public subs

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4Send)
    def onRecieve(self, event: Msg4Send):
        if event.recieverId == self.myId:
            self._updateClock(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4Broadcast)
    def onBroadcast(self, event: Msg4Broadcast):
        if event.senderId != self.myId:
            self._updateClock(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Token)
    def onToken(self, event: Token):
        if event.holderId == self.myId:
            self._updateClock(event)
            self.token = event
            self.manageToken()

    # region Private subs

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4Ready)
    def onReady(self, event: Msg4Ready):
        self._updateClock(event)
        self._countReady +=1
        if self._countReady == self.nbProcess:
            self._broadcastAllReady()
    

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4AllReady)
    def onAllReady(self, event: Msg4AllReady):
        self._updateClock(event)
        self._countReady = self.nbProcess + 1
    


    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4IdConsensus)
    def onIdConsensus(self, event: Msg4IdConsensus):
        self._updateClock(event)
        
    
    # endregion Private subs



    # region Public post

    def sendTo(self, msg: Any, toId: int):
        self.post(
            Msg4Send(msg,
                    self.clock,
                    toId)
        )

    def broadcast(self, msg: Any):
        self.post(
            Msg4Broadcast(msg,
                        self.clock,
                        self.myId)
        )

    # endregion Public post

    # region Private post

    def _broadcastReady(self):
        self.post(
            Msg4Ready(None, 
                      self.clock)
        )
    
    def _broadcastAllReady(self):
        self.post(
            Msg4AllReady(None, 
                      self.clock)
        )

    # endregion Private post


    def _updateClock(self, msg:Msg):
        self.clock = max(self.clock, msg.timestamp) + 1

    def _findIdConsensus(self):
        preId = random.randint(0, 10000 * self.nbProcess)
        self.post(Msg4IdConsensus)



    def manageToken(self):
        while self.token:
            sleep(0.01)
            if not self.token.isInUse:
                self.transfereToken()

    def requestSC(self):
        while not self.token:
            sleep(0.01)
        self.token.use()

    def releaseSC(self):
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

    def post(self, msg: Msg):
        self.clock += 1
        PyBus.Instance().post(msg)

    def nextId(self):
        return (self.myId + 1) % self.nbProcess


    def stop(self):
        self.alive = False


