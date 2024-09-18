class Token:
    def __init__(self, holderId: int) -> None:
        self.holderId = holderId
        self.isInUse = False

    def changeHolder(self, holderId: int):
        self.holderId = holderId
        self.isInUse = False
        return self

    def use(self):
        self.isInUse = True

    def release(self):
        self.isInUse = False
