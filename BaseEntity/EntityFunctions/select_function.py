from abc import ABC, abstractmethod
from enum import Enum

class Select(ABC):

    def __init__(self, id: str):
        self.id = id
