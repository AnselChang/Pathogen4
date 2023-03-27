from abc import ABC, abstractmethod

class Click(ABC):

    @abstractmethod
    def onLeftClick(self):
        pass

    @abstractmethod
    def onRightClick(self):
        pass

class ClickLambda(Click):

    def __init__(self, FonLeftClick = lambda: None, FonRightClick = lambda: None):
        self.FonLeftClick = FonLeftClick
        self.FonRightClick = FonRightClick

    def onLeftClick(self):
        self.FonLeftClick()

    def onRightClick(self):
        self.FonRightClick()