from reference_frame import PointRef, Ref
from BaseEntity.EntityListeners.click_listener import ClickLambda
from UIEntities.radio_entity import RadioEntity

from math_functions import isInsideBox2
from pygame_functions import drawSurface, brightenSurface
from dimensions import Dimensions
from draw_order import DrawOrder
from Tooltips.tooltip import TooltipOwner, Tooltip
import pygame

"""
Easily create image radio options through this class
Either pass in integers to (xIntOrCallback, yIntOrCallback),
or pass in functions for getters of x and y
"""
class ImageRadioEntity(RadioEntity, TooltipOwner):

    # id is used to distinguish between radio entities
    def __init__(self, id: str, imageOn: pygame.Surface, imageOff: pygame.Surface, tooltip: str | list[str] = None, onUpdate = lambda isOn: None):
        super().__init__(id, DrawOrder.UI_BUTTON, onUpdate = onUpdate)

        self.width = imageOn.get_width()
        self.height = imageOn.get_height()

        HOVER_DELTA = 50
        self.imageOn = {False: imageOn, True: brightenSurface(imageOn, HOVER_DELTA)}
        self.imageOff = {False: imageOff, True: brightenSurface(imageOff, HOVER_DELTA)}

        if tooltip is None:
            self.tooltip = None
        else:
            self.tooltip = Tooltip(tooltip)

    def getTooltip(self) -> Tooltip | None:
        return self.tooltip

    def isTouching(self, position: PointRef) -> bool:
        x,y = self.getPositionRaw()
        return isInsideBox2(*position.screenRef, x - self.width/2, y - self.height/2, self.width, self.height)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        x,y = self.getPositionRaw()
        image = self.imageOn if self is self.group.getActiveEntity() else self.imageOff
        drawSurface(screen, image[isHovered], x, y)
            