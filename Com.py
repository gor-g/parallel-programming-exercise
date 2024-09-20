from time import sleep
from typing import Any
import random
from pyeventbus3.pyeventbus3 import PyBus, subscribe, Mode
from Token import Token
from Msg import *

class Com:
    def __init__(self, nbProcess):
        self.myId = None
        self.nbProcess = nbProcess
        PyBus.Instance().register(self, self)
        self.clock = 0
        self.alive = True
        self.token:None | Token = None

        self._countReady = 0
        self._allReady = False
        self._preId = None
        self._preIds = []

        self._isSynchronizing = False
        self._syncCounter = 0






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

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4TokenTransfere)
    def onToken(self, event: Msg4TokenTransfere):
        if event.payload.holderId == self.myId:
            self._updateClock(event)
            self.token = event.payload
            self.manageToken()


    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4Synchronize)
    def onSynchronize(self, event: Msg4Synchronize):
        self._updateClock(event)
        self._isSynchronizing = True
        self._syncCounter += 1
        if self._syncCounter == self.nbProcess:
            self._post(
                Msg4SynchronizeDone(
                self.myId
            ))

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4SynchronizeDone)
    def onSynchronizeDone(self, event: Msg4SynchronizeDone):
        self._updateClock(event)
        self._syncCounter = 0
        self._isSynchronizing = False

    # region Private subs

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4Ready)
    def onReady(self, event: Msg4Ready):
        self._updateClock(event)
        self._countReady = min(self._countReady+1, self.nbProcess)
        if self._countReady == self.nbProcess:
            self._broadcastAllReady()

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4AllReady)
    def onAllReady(self, event: Msg4AllReady):
        self._updateClock(event)
        self._countReady = self.nbProcess
        self._findIdConsensus()

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Msg4IdConsensus)
    def onIdConsensus(self, event: Msg4IdConsensus):
        self._updateClock(event)
        self._preIds.append(event.payload)
    
    # endregion Private subs



    # region Public post

    def sendTo(self, msg: Any, toId: int):
        self._post(
            Msg4Send(msg,   
                     toId)
        )

    def broadcast(self, msg: Any):
        self._post(
            Msg4Broadcast(msg,
                          self.myId)
        )

    def synchronize(self):
        self._post(
            Msg4Synchronize(None, self.myId, self.nextId())
        )
        self._isSynchronizing = True
        while self._isSynchronizing:
            sleep(0.01)
        


    # endregion Public post

    # region Private post

    def _broadcastReady(self):
        self._post(Msg4Ready(None))
    
    def _broadcastAllReady(self):
        self._post(Msg4AllReady(None))

    # endregion Private post


    def _updateClock(self, msg:Msg):
        self.clock = max(self.clock, msg.timestamp) + 1

    def _findIdConsensus(self):
        self._preId = random.randint(0, 10000 * self.nbProcess)
        self._post(Msg4IdConsensus(self._preId))
        sleep(1)
        if len(set(self._preIds))!=self.nbProcess:
            self._preIds = []
            sleep(1)
            self._findIdConsensus()
        else:
            self._preIds.sort()
            self.myId = self._preIds.index(self._preId)


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
        self._post(
            Msg4TokenTransfere(
                    self.token.changeHolder(
                        self.nextId()
                )
            )
            
        )
        self.token = None

    def launchToken(self):
        self._post(
            Msg4TokenTransfere(
                Token(self.myId)
            )
        )

    def _post(self, msg: Msg):
        self.clock += 1
        msg.setStamp(self.clock)
        PyBus.Instance().post(msg)

    def nextId(self):
        return (self.myId + 1) % self.nbProcess

    def prevId(self):
        return (self.myId - 1) % self.nbProcess


    def stop(self):
        self.alive = False


