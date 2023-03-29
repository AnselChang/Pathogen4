from Adapters.adapter import Adapter

"""
Stores a path variable name, as well as a location
Get text by finding variable value through the adapter
"""

class Readout:
    def __init__(self, variableName: str, dx: int, dy: int):
        self.variableName = variableName
        self.dx = dx
        self.dy = dy

    def getValue(self, adapter: Adapter) -> str:
        return str(adapter.get(self.variableName))