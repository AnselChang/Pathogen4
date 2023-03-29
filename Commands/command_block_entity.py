from BaseEntity.entity import Entity
from Adapters.adapter import Adapter
from reference_frame import PointRef, Ref
from Commands.command_state import CommandState
import pygame



class CommandBlockEntity(Entity):
    
    def __init__(self, state: CommandState):
        self.setState(state)

    def setState(self, state: CommandState):
        self.state = state

    def isVisible(self) -> bool:
        pass

    def isTouching(self, position: PointRef) -> bool:
        pass

    def distanceTo(self, position: PointRef) -> float:
        return (position - self.getPosition()).magnitude(Ref.SCREEN)

    def getPosition(self) -> PointRef:
        pass

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    def toString(self) -> str:
        pass
