from reference_frame import PointRef, Ref
from BaseEntity.EntityListeners.click_listener import ClickLambda
from UIEntities.Generic.radio_entity import RadioEntity

from math_functions import isInsideBox2
from pygame_functions import drawText
from draw_order import DrawOrder
from font_manager import DynamicFont
import pygame

# Subclasses implement: isTouching, distanceTo, draw
class TabEntity(RadioEntity):

    # id is used to distinguish between radio entities
    def __init__(self, font: DynamicFont, text: str):
        super().__init__(text, DrawOrder.TAB)

        self.font = font

        self.y = 2
        self.height = 30

        self.text = text
        self.r = 5

    def defineCenter(self) -> tuple:
        return self._px(0), self._py(0.5)

    def defineWidth(self) -> float:
        return self._pwidth(1) / self.group.N
    def defineHeight(self) -> float:
        return self._pheight(1)

    def isTouching(self, position: tuple) -> bool:
        return isInsideBox2(*position, *self.RECT)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        if self is self.group.getActiveEntity():
            color = (150, 150, 150)
        elif isHovered:
            color = (180, 180, 180)
        else:
            color = (200, 200, 200)
        pygame.draw.rect(screen, color, self.RECT,
                         border_top_left_radius = self.r, border_top_right_radius = self.r)
        
        # draw border. black if selected
        color = (0,0,0) if self.isActive() else (100,100,100)
        pygame.draw.rect(screen, color, self.RECT,
                         border_top_left_radius = self.r, border_top_right_radius = self.r, width = 1)
        
        drawText(screen, self.font.get(), self.text, (0,0,0), self.CENTER_X, self.CENTER_Y)