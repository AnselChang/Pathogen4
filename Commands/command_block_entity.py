from BaseEntity.entity import Entity
from Adapters.adapter import Adapter
from reference_frame import PointRef, Ref
from Commands.command_state import CommandState
from draw_order import DrawOrder
import pygame



class CommandBlockEntity(Entity):
    
    def __init__(self, state: CommandState):
        super().__init__(drawOrder = DrawOrder.COMMANND_BLOCK)
        self.setState(state)

    def setState(self, state: CommandState):
        self.state = state

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return False

    def getPosition(self) -> PointRef:
        pass

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    def toString(self) -> str:
        pass
