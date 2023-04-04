from reference_frame import PointRef, Ref
from BaseEntity.EntityListeners.click_listener import ClickLambda
from UIEntities.radio_entity import RadioEntity

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

    def getCenter(self) -> tuple:
        return self.dimensions.FIELD_WIDTH, 0

    # must impl both of these if want to contain other entity
    def getWidth(self) -> float:
        return self.dimensions.PANEL_WIDTH
    def getHeight(self) -> float:
        return self.dimensions.SCREEN_HEIGHT

    def isVisible(self) -> bool:
        return True
    
    def getRect(self) -> tuple:
        x,y = self.getPosition().screenRef
        width = self.getWidth()
        return (x - width/2, y - self.height/2, width, self.height)

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, *self.getRect())

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        rect = self.getRect()

        if self is self.group.getActiveEntity():
            color = (150, 150, 150)
        elif isHovered:
            color = (180, 180, 180)
        else:
            color = (200, 200, 200)
        pygame.draw.rect(screen, color, rect,
                         border_top_left_radius = self.r, border_top_right_radius = self.r)
        
        # draw border. black if selected
        color = (0,0,0) if self.isActive() else (100,100,100)
        pygame.draw.rect(screen, color, rect,
                         border_top_left_radius = self.r, border_top_right_radius = self.r, width = 1)
        
        drawText(screen, self.font.get(), self.text, (0,0,0), *self.getPosition().screenRef)