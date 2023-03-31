from BaseEntity.entity import Entity
from Adapters.path_adapter import PathAdapter

"""
Stores a path variable name, as well as a location
Get text by finding variable value through the adapter
"""

class ReadoutEntity(Entity):
    def __init__(self, variableName: str, dx: int, dy: int):
        self.variableName = variableName
        self.dx = dx
        self.dy = dy

    def getValue(self, adapter: PathAdapter) -> str:
        return str(adapter.get(self.variableName))