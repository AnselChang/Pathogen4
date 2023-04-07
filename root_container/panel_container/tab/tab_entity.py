from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.tab.tab_group_entity import TabGroupEntity

from common.reference_frame import PointRef, Ref
from entity_base.listeners.click_listener import ClickLambda
from entity_base.text_entity import TextEntity
from entity_ui.group.radio_entity import RadioEntity

from utility.math_functions import isInsideBox2
from utility.pygame_functions import drawText
from common.draw_order import DrawOrder
from common.font_manager import FontID
import pygame

# Subclasses implement: isTouching, distanceTo, draw
class TabEntity(RadioEntity):

    # id is used to distinguish between radio entities
    def __init__(self, group: TabGroupEntity, text: str):
        super().__init__(group, text)
        self.recomputePosition()

        self.r = 5

        TextEntity(self, FontID.FONT_NORMAL, 10, staticText = text)

    def defineWidth(self) -> float:
        return self._getSubdivision() - self._aheight(1)
    def defineHeight(self) -> float:
        return self._pheight(1)


    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:


        isActive = self.group.isOptionOn(self)

        if isActive:
            color = (150, 150, 150)
        elif isHovered:
            color = (180, 180, 180)
        else:
            color = (200, 200, 200)
        pygame.draw.rect(screen, color, self.RECT,
                         border_top_left_radius = self.r, border_top_right_radius = self.r)
        
        # draw border. black if selected
        color = (0,0,0) if isActive else (100,100,100)
        pygame.draw.rect(screen, color, self.RECT,
                         border_top_left_radius = self.r, border_top_right_radius = self.r, width = 1)
        