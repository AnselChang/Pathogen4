from abc import ABC, abstractmethod

"""
For mousewheel events.
Return true if entity handles it. Otherwise, it will go up
the chain of parent entities until someone handles it
"""

class MousewheelListener(ABC):

    def __init__(self, entity):
        self.entity = entity

        self.mouse: tuple = None

    # return true if handled by entity
    @abstractmethod
    def onMousewheel(self, offset):
        return False


class MousewheelLambda(MousewheelListener):

    def __init__(self, entity, FonMousewheel = lambda: bool):
        super().__init__(entity)

        self.FonMousewheel = FonMousewheel

    def onMousewheel(self, offset) -> bool:
        return self.FonMousewheel(offset)