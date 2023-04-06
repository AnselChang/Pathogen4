from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.command_or_inserter import CommandOrInserter

from entity_handler.interactor import Interactor

from global.dimensions import Dimensions
from data_structures.linked_list import LinkedListNode
from global.reference_frame import PointRef, Ref
from global.draw_order import DrawOrder

from utility.math_functions import isInsideBox2

import pygame

"""
Appears between each command
A "plus" button that, when clicked, inserts a custom command there
"""

class CommandInserter(Entity, CommandOrInserter):

    def __init__(self, path, onInsert = lambda: None):

        super().__init__(
            hover = HoverLambda(self, FonHoverOn = self.onHoverOn, FonHoverOff = self.onHoverOff),
            click = ClickLambda(self, FonLeftClick = lambda: onInsert(self)),
            select = SelectLambda(self, "inserter", type = SelectorType.SOLO),
            drawOrder = DrawOrder.COMMAND_INSERTER)
        CommandOrInserter.__init__(self)

        self.path = path

        self.START_Y = 43
        self.Y_MIN = 6
        self.Y_MAX = 15

        # shaded area specs
        self.X_MARGIN_LEFT = 6
        self.X_MARGIN_RIGHT = 18
        self.Y_MARGIN = 3
        self.CORNER_RADIUS = 3
        self.MOUSE_MARGIN = 0

        # cross specs
        self.RADIUS = 6
        self.HOVER_RADIUS = 8
        self.THICK = 3 # cross thick radius
        self.THIN = 1 # cross thin radius

        self.currentY = self.START_Y
        self.isActive = False

    def defineTopLeft(self) -> tuple:
        # right below the previous CommandOrInserter
        return self._px(0), self._py(1)

    def defineWidth(self) -> float:
        # 95% of the panel
        return self._pwidth(self.WIDTH_PERCENT_OF_PANEL)
    
    def defineHeight(self) -> float:
        P_HEIGHT_MIN = 0.001
        P_HEIGHT_MAX = 0.025
        return self._pheight(P_HEIGHT_MAX if self.isActive else P_HEIGHT_MIN)

    def setActive(self, isActive):
        self.isActive = isActive
        self.recomputePosition()

    def onHoverOn(self):

        if len(self.interactor.selected.entities) > 1 or self.interactor.leftDragging or self.interactor.rightDragging:
            return

        self.setActive(True)

    def onHoverOff(self):
        if self.isActive:
            self.setActive(False)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        isActive = isActive and self.interactor.leftDragging and self.isActive
        
        if isActive or self.isActive:
            
            color = [140, 140, 140] if isActive else [160, 160, 160]

            # draw shaded area
            pygame.draw.rect(screen, color, self.RECT, border_radius = self.CORNER_RADIUS)

            # draw cross
            x,y = self.CENTER_X, self.CENTER_Y
            pygame.draw.rect(screen, [255,255,255], [x - self.THICK, y - self.THIN, self.THICK*2, self.THIN*2])
            pygame.draw.rect(screen, [255,255,255], [x - self.THIN, y - self.THICK, self.THIN*2, self.THICK*2])