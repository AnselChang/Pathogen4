from reference_frame import PointRef, Ref
from BaseEntity.EntityListeners.click_listener import ClickLambda
from UIEntities.Generic.radio_entity import RadioEntity

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
    def __init__(self, px: float, py: float, imageOn: pygame.Surface, imageOff: pygame.Surface, tooltip: str | list[str] = None, onUpdate = lambda isOn: None):
        super().__init__(id, DrawOrder.UI_BUTTON, onUpdate = onUpdate)

        self.px = px
        self.py = py

        HOVER_DELTA = 50
        self.imageOn = {False: imageOn, True: brightenSurface(imageOn, HOVER_DELTA)}
        self.imageOff = {False: imageOff, True: brightenSurface(imageOff, HOVER_DELTA)}

        if tooltip is None:
            self.tooltip = None
        else:
            self.tooltip = Tooltip(tooltip)

        self.recomputePosition()

    # impl EITHER getCenter OR getTopLeft
    def defineCenter(self) -> tuple:
        return self._px(self.px), self._py(self.py)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self.imageOn.get_width()
    def defineHeight(self) -> float:
        return self.imageOn.get_height()
        

    def getTooltip(self) -> Tooltip | None:
        return self.tooltip

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        image = self.imageOn if self is self.group.getActiveEntity() else self.imageOff
        drawSurface(screen, image[isHovered], self.CENTER_X, self.CENTER_Y)
            