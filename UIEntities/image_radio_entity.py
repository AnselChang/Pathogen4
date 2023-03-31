from reference_frame import PointRef, Ref
from BaseEntity.EntityListeners.click_listener import ClickLambda
from UIEntities.radio_entity import RadioEntity

from math_functions import isInsideBox2
from pygame_functions import drawSurface, brightenSurface
from dimensions import Dimensions
from draw_order import DrawOrder
import pygame

# Subclasses implement: isTouching, distanceTo, draw
class ImageRadioEntity(RadioEntity):

    # id is used to distinguish between radio entities
    def __init__(self, id: str, imageOn: pygame.Surface, imageOff: pygame.Surface, xIntOrCallback: int, yIntOrCallback: int, onUpdate = lambda isOn: None):
        super().__init__(id, DrawOrder.UI_BUTTON, onUpdate = onUpdate)

        self.xIntOrCallback, self.yIntOrCallback = xIntOrCallback, yIntOrCallback
        self.width = imageOn.get_width()
        self.height = imageOn.get_height()

        HOVER_DELTA = 50
        self.imageOn = {False: imageOn, True: brightenSurface(imageOn, HOVER_DELTA)}
        self.imageOff = {False: imageOff, True: brightenSurface(imageOff, HOVER_DELTA)}

    def getPositionRaw(self) -> tuple:
        x = self.xIntOrCallback if type(self.xIntOrCallback) == int else self.xIntOrCallback()
        y = self.yIntOrCallback if type(self.yIntOrCallback) == int else self.yIntOrCallback() 
        return x, y 

    # override
    def getPosition(self) -> PointRef:
        x,y = self.getPositionRaw()
        return PointRef(Ref.SCREEN, (x, y))

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        x,y = self.getPositionRaw()
        return isInsideBox2(*position.screenRef, x - self.width/2, y - self.height/2, self.width, self.height)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        x,y = self.getPositionRaw()
        image = self.imageOn if self is self.group.getActiveEntity() else self.imageOff
        drawSurface(screen, image[isHovered], x, y)
            