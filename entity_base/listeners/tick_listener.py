from abc import ABC, abstractmethod

"""
Tick callbacks are invoked on a recursive manner. onTickStart() callbacks
are invoked on the parent entities before children, while onTickEnd() callbacks
are invoked on the children before the parent.
"""

class TickListener(ABC):

    def __init__(self, entity):
        self.entity = entity

    @abstractmethod
    def onTickStart(self):
        pass

    @abstractmethod
    def onTickEnd(self):
        pass


class TickLambda(TickListener):

    def __init__(self, entity, FonTickStart = lambda: None, FonTickEnd = lambda: None):
        super().__init__(entity)

        self.FonTickStart = FonTickStart
        self.FonTickEnd = FonTickEnd

    def onTickStart(self):
        self.FonTickStart()

    def onTickEnd(self):
        self.FonTickEnd()