from abc import ABC, abstractmethod

class ClickListener(ABC):

    def __init__(self, entity):
        self.entity = entity

    @abstractmethod
    def onMouseDown(self, mouse: tuple):
        pass


    @abstractmethod
    def onLeftClick(self, mouse: tuple):
        pass

    @abstractmethod
    def onRightClick(self, mouse: tuple):
        pass

    @abstractmethod
    def onDoubleLeftClick(self, mouse: tuple):
        pass

class ClickLambda(ClickListener):

    def __init__(self, entity, FonLeftClick = lambda mouse: None,
                 FonRightClick = lambda mouse: None,
                 FOnDoubleClick = lambda mouse: None,
                 FOnMouseDown = lambda mouse: None,
                 ):
        super().__init__(entity)

        self.FonLeftClick = FonLeftClick
        self.FonRightClick = FonRightClick
        self.FOnDoubleClick = FOnDoubleClick
        self.FOnMouseDown = FOnMouseDown

    def onMouseDown(self, mouse: tuple):
        return self.FOnMouseDown(mouse)

    def onLeftClick(self, mouse: tuple):
        return self.FonLeftClick(mouse)

    def onRightClick(self, mouse: tuple):
        return self.FonRightClick(mouse)

    def onDoubleLeftClick(self, mouse: tuple):
        return self.FOnDoubleClick(mouse)
    