"""
An entity used for testing that is simply a rectangle
"""

from common.draw_order import DrawOrder
from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
import pygame

class TestRectEntity(Entity):
    
    def __init__(self, parent: VariableGroupContainer, width, height, color):

        super().__init__(parent = parent,
                         hover = HoverLambda(self, FonHoverOn = self.onHoverOn, FonHoverOff = self.onHoverOff),
                         drawOrder = DrawOrder.FRONT)
        self.color = color

        self.width = width
        self.baseHeight = height
        self.height = self.baseHeight
        self.parentContainer = parent

    def onHoverOn(self):
        self.height = self.baseHeight * 1.5
        self.parentContainer.onChangeInContainerSize()

    def onHoverOff(self):
        self.height = self.baseHeight
        self.parentContainer.onChangeInContainerSize()

    def defineWidth(self) -> float:
        return self._awidth(self.width)
    
    def defineHeight(self) -> float:
        return self._aheight(self.height)
    
    def defineCenterX(self) -> float:
        return self._px(0.5)

    def draw(self, screen, isActive, isHovering):
        pygame.draw.rect(screen, (0, 0, 0), self.RECT, 2)
