from reference_frame import PointRef, Ref
from BaseEntity.EntityFunctions.click_function import ClickLambda
from UIEntities.radio_entity import RadioEntity

from math_functions import isInsideBox2
from pygame_functions import drawText, FONT15
from dimensions import Dimensions
from draw_order import DrawOrder
import pygame

# Subclasses implement: isTouching, distanceTo, draw
class TabEntity(RadioEntity):

    # id is used to distinguish between radio entities
    def __init__(self, dimensions: Dimensions, text: str, tabID: int, numTabs: int):
        super().__init__(text, DrawOrder.TAB)

        self.dimensions = dimensions

        self.tabID = tabID
        self.numTabs = numTabs

        self.y = 2
        self.height = 30

        self.text = text
        self.r = 5

    # override
    def getPosition(self) -> PointRef:
        x = self.dimensions.FIELD_WIDTH + (self.dimensions.PANEL_WIDTH) / (self.numTabs) * (self.tabID + 0.5)
        return PointRef(Ref.SCREEN, (x,self.y + self.height/2))
    
    def getWidth(self) -> int:
        return (self.dimensions.PANEL_WIDTH) / (self.numTabs) - 1

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

        if self is self.group.getEntity():
            color = (150, 150, 150)
        elif isHovered:
            color = (180, 180, 180)
        else:
            color = (200, 200, 200)
        pygame.draw.rect(screen, color, rect,
                         border_top_left_radius = self.r, border_top_right_radius = self.r)
        
        # draw border. black if selected
        color = (0,0,0) if self is self.group.getEntity() else (100,100,100)
        pygame.draw.rect(screen, color, rect,
                         border_top_left_radius = self.r, border_top_right_radius = self.r, width = 1)
        
        drawText(screen, FONT15, self.text, (0,0,0), *self.getPosition().screenRef)