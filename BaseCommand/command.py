from abc import ABC, abstractmethod
from BaseCommand.widget import Widget

class Command(ABC):

    

    @abstractmethod
    def getGeneratedCode(self) -> str:
        pass