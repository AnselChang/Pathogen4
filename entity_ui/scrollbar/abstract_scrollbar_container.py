from entity_base.container_entity import Container
from entity_ui.scrollbar.scrollbar_entity import ScrollbarEntity

from common.draw_order import DrawOrder

from data_structures.observer import Observable
from utility.math_functions import isInsideBox2

import pygame

"""
Subclass this with define[Position] functions for concrete scroller containers
Subscribers will be notified when scrollbar position changes
"""
class AbstractScrollbarContainer(Container, Observable):

    def __init__(self, parent):

        super().__init__(parent = parent, drawOrder = DrawOrder.SCROLLBAR_BORDER)
        self.recomputePosition()

        # after position of container has been computed, add scrollbar entity
        self.scrollbar = ScrollbarEntity(self)

        # anyone who subscribes to scrollbar container is essentially subscribed to scrollbar entity
        self.scrollbar.subscribe(onNotify = self.notify)
        
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        color = [0,0,0]
        pygame.draw.rect(screen, color, self.RECT, 1)