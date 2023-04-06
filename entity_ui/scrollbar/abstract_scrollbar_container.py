from entity_base.container_entity import Container
from entity_ui.scrollbar.scrollbar_entity import ScrollbarEntity

from common.draw_order import DrawOrder

from data_structures.observer import Observable
from utility.math_functions import isInsideBox2

import pygame

"""
Subclass this with define[Position] functions for concrete scroller containers
"""
class AbstractScrollbarContainer(Container):

    def __init__(self, parent):

        super().__init__(parent = parent, drawOrder = DrawOrder.SCROLLBAR_BACKGROUND)
        self.recomputePosition()

        # after position of container has been computed, add scrollbar entity
        self.scrollbar = ScrollbarEntity(self)
        