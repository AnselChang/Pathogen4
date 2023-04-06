from BaseEntity.entity import Entity
from Commands.command_block_icon import CommandBlockIcon
from Adapters.path_adapter import PathAdapter
from draw_order import DrawOrder

class CommandBlockHeader(Entity):

    def __init__(self, pathAdapter: PathAdapter):
        super().__init__(drawOrder = DrawOrder.WIDGET)

        self.entities.addEntity(CommandBlockIcon(pathAdapter), self)

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pwidth(1)
    def defineHeight(self) -> float:
        return self._parent.COLLAPSED_HEIGHT