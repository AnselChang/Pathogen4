from abc import ABC, abstractmethod

class Click(ABC):

    @abstractmethod
    def onClick(self):
        pass

class ClickLambda(Click):

    def __init__(self, FonClick = lambda: None):
        self.FonClick = FonClick

    def onClick(self):
        self.FonClick()