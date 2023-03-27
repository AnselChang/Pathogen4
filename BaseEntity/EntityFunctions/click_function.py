from abc import ABC, abstractmethod

class Click(ABC):

    @abstractmethod
    def onClick(self):
        pass
