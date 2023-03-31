from BaseEntity.entity import Entity
from Adapters.path_adapter import PathAdapter

from Widgets.defined_readout import DefinedReadout

from reference_frame import PointRef, Ref
from draw_order import DrawOrder
from pygame_functions import drawText, FONT15
import pygame

"""
Belongs to a specific CommandBlockEntity.
Owns a DefinedReadout which stores information about the widget's context for all commands of that type
"""

class ReadoutEntity(Entity):
    def __init__(self, parentCommand: Entity, definedReadout: DefinedReadout, pathAdapter: PathAdapter):

        super().__init__(drawOrder = DrawOrder.READOUT)

        self.parentCommand = parentCommand
        self.definedReadout = definedReadout
        self.pathAdapter = pathAdapter

    def getText(self) -> str:
        return str(self.pathAdapter.get(self.definedReadout.getAttribute()))
    
    def isVisible(self) -> bool:
        return self.parentCommand.isVisible()

    # not interactable
    def isTouching(self, position: PointRef) -> bool:
        return False
    
    def getPosition(self) -> PointRef:
        px, py = self.definedReadout.getPositionRatio()
        x = self.parentCommand.getX() + px * self.parentCommand.getWidth()
        y = self.parentCommand.getY() + py * self.parentCommand.getHeight()
        return PointRef(Ref.SCREEN, (x, y))
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        # opacity: 1 = solid, 0 = invisible
        opacity = self.parentCommand.getAddonsOpacity()
        drawText(screen, FONT15, self.getText(), (0,0,0), *self.getPosition().screenRef, opacity = opacity)

    def toString(self) -> str:
        return "Readout entity"