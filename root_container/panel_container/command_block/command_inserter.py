from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.path import Path

from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.command_or_inserter import CommandOrInserter

from entity_handler.interactor import Interactor

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

class CommandInserter(Entity, CommandOrInserter):

    def __init__(self, parent: CommandOrInserter, path: Path, onInsert = lambda: None, isFirst: bool = False):
        super().__init__(
            parent = parent,
            hover = HoverLambda(self, FonHoverOn = self.onHoverOn, FonHoverOff = self.onHoverOff),
            click = ClickLambda(self, FonLeftClick = lambda mouse: onInsert(self)),
            select = SelectLambda(self, "inserter", type = SelectorType.SOLO),
            drawOrder = DrawOrder.COMMAND_INSERTER)
        CommandOrInserter.__init__(self, False)

        self.path = path
        self.isFirst = isFirst

        self.START_Y = 43
        self.Y_MIN = 6
        self.Y_MAX = 15

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

        self.recomputePosition()

    def defineTopLeft(self) -> tuple:

        # This prevents the ripple effect when inserting a command
        # by using the parent's target position directly instead of their current
        if not self.isFirst:
            y = self._parent.normalY + self._pheight(1)
        else:
            y = self._py(0)

        # right below the previous CommandOrInserter
        return self._px(0), y

    def defineWidth(self) -> float:
        # 95% of the panel
        return self._pwidth(1)
    
    def defineHeight(self) -> float:
        HEIGHT_MIN = 5
        HEIGHT_MAX = 12
        return self._aheight(HEIGHT_MAX if self.isActive else HEIGHT_MIN)

    def setActive(self, isActive):
        self.isActive = isActive
        self.path.onChangeInCommandPositionOrHeight()

    def onHoverOn(self):

        if len(self.interactor.selected.entities) > 1 or self.interactor.leftDragging or self.interactor.rightDragging:
            return

        self.setActive(True)

    def onHoverOff(self):
        if self.isActive:
            self.setActive(False)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        isActive = isActive and self.interactor.leftDragging and self.isActive

        Y_MARGIN = 2
        rect = [self.LEFT_X, self.TOP_Y + Y_MARGIN, self.WIDTH, self.HEIGHT - Y_MARGIN*2]
        
        if isActive or self.isActive:
            
            color = [140, 140, 140] if isActive else [160, 160, 160]

            # draw shaded area
            pygame.draw.rect(screen, color, rect, border_radius = self.CORNER_RADIUS)

            # draw cross
            x,y = self.CENTER_X, self.CENTER_Y
            pygame.draw.rect(screen, [255,255,255], [x - self.THICK, y - self.THIN, self.THICK*2, self.THIN*2])
            pygame.draw.rect(screen, [255,255,255], [x - self.THIN, y - self.THICK, self.THIN*2, self.THICK*2])