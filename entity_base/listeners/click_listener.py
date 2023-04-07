from abc import ABC, abstractmethod

class ClickListener(ABC):

    def __init__(self, entity):
        self.entity = entity

    @abstractmethod
    def onLeftClick(self, mouse: tuple):
        pass

    @abstractmethod
    def onRightClick(self, mouse: tuple):
        pass

    @abstractmethod
    def onDoubleLeftClick(self):
        pass

class ClickLambda(ClickListener):

    def __init__(self, entity, FonLeftClick = lambda mouse: None,
                 FonRightClick = lambda mouse: None,
                 FOnDoubleClick = lambda mouse: None):
        super().__init__(entity)

        self.FonLeftClick = FonLeftClick
        self.FonRightClick = FonRightClick
        self.FOnDoubleClick = FOnDoubleClick

    def onLeftClick(self, mouse: tuple):
        self.FonLeftClick(mouse)

    def onRightClick(self, mouse: tuple):
        self.FonRightClick(mouse)

    def onDoubleLeftClick(self, mouse: tuple):
        self.FOnDoubleClick(mouse)