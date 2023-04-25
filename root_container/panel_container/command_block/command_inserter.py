from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity_ui.group.variable_group.variable_container import VariableContainer
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler


from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_handler.interactor import Interactor

from root_container.panel_container.command_block.command_block_constants import CommandBlockConstants as Constants

from common.dimensions import Dimensions
from data_structures.linked_list import LinkedListNode
from common.reference_frame import PointRef, Ref
from common.draw_order import DrawOrder

from utility.math_functions import isInsideBox2

import pygame

"""
Appears between each command
A "plus" button that, when clicked, inserts a custom command there
"""

class CommandInserter(Entity):

    def __init__(self, parent: VariableContainer, handler: CommandSequenceHandler, onInsert = lambda: None, isFirst: bool = False):
        super().__init__(
            parent = parent,
            hover = HoverLambda(self, FonHoverOn = self.onHoverOn, FonHoverOff = self.onHoverOff),
            click = ClickLambda(self, FonLeftClick = lambda mouse: onInsert(self)),
            select = SelectLambda(self, "inserter", type = SelectorType.SOLO),
            drawOrder = DrawOrder.COMMAND_INSERTER,
            recomputeWhenInvisible = True
            )
        
        self.container = parent
        self.handler = handler
        self.isFirst = isFirst

        self.START_Y = 43

        # shaded area specs
        self.X_MARGIN_LEFT = 6
        self.X_MARGIN_RIGHT = 18
        self.Y_MARGIN = 3
        self.MOUSE_MARGIN = 0

        # cross specs
        self.RADIUS = 6
        self.HOVER_RADIUS = 8
        self.THICK = 3 # cross thick radius
        self.THIN = 1 # cross thin radius

        self.currentY = self.START_Y
        self.isActive = False
        self.hovering = False

    def defineCenterX(self) -> tuple:
        return self._px(0.5)

    def defineWidth(self) -> float:
        # 95% of the panel
        return self._pwidth(1)
    
    def defineHeight(self) -> float:

        if not self.isFirst and self.getPreviousCommand() is not None and not self.getPreviousCommand().isVisible():
            return 0

        if self.handler.isOnlyInserter(self):
            HEIGHT_MIN = 30
            HEIGHT_MAX = 30
        else:
            HEIGHT_MIN = 5
            HEIGHT_MAX = 12
        return self._aheight(HEIGHT_MAX if self.hovering else HEIGHT_MIN)
    

    def setActive(self, isActive):
        self.isActive = isActive
        self.propagateChange()

    def defineBefore(self):
        if self.getPreviousCommand() is None or self.getPreviousCommand().isVisible():
            self.setActive(True)
        else:
            self.setActive(False)

    def onHoverOn(self):

        if len(self.interactor.selected.entities) > 1 or self.interactor.leftDragging or self.interactor.rightDragging:
            return

        if self.isActive:
            self.hovering = True
            self.propagateChange()

    def onHoverOff(self):
        self.hovering = False
        self.propagateChange()

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        isActive = isActive and self.interactor.leftDragging and self.isActive

        Y_MARGIN = 2
        rect = [self.LEFT_X, self.TOP_Y + Y_MARGIN, self.WIDTH, self.HEIGHT - Y_MARGIN*2]
        
        isOnlyInserter = self.handler.isOnlyInserter(self)

        if self.isActive and (self.hovering or isOnlyInserter):
            
            color = [140, 140, 140] if (self.hovering) else [160, 160, 160]

            # draw shaded area
            pygame.draw.rect(screen, color, rect, border_radius = Constants.CORNER_RADIUS)

            # draw cross
            x,y = self.CENTER_X, self.CENTER_Y
            pygame.draw.rect(screen, [255,255,255], [x - self.THICK, y - self.THIN, self.THICK*2, self.THIN*2])
            pygame.draw.rect(screen, [255,255,255], [x - self.THIN, y - self.THICK, self.THIN*2, self.THICK*2])

    def getPreviousCommand(self):
        return self.handler.getPrevious(self)
    
    def getNextCommand(self):
        return self.handler.getNext(self)