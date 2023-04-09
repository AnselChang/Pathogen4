from enum import Enum
from entity_base.image.image_state import ImageState
from entity_base.listeners.click_listener import ClickLambda
from entity_base.entity import Entity

from utility.pygame_functions import drawSurface
from common.draw_order import DrawOrder
from entity_ui.tooltip import TooltipOwner, Tooltip
from common.image_manager import ImageID
import pygame


"""
A generic image entity, where you pass in images
Is drawn to fit inside parent entity's rect
"""
class ImageEntity(Entity, TooltipOwner):

    # px, py, pwidth, pheight set by default to the dimensions of the parent
    def __init__(self, parent, states: ImageState | list[ImageState], drawOrder: DrawOrder,
                 onClick = lambda mouse: None, dimOnHover: bool = True,
                 center_px = 0.5, center_py = 0.5, pwidth = 1, pheight = 1,
                 isOn = lambda: True,
                 getStateID = lambda: None,
                 drag = None
                ):
        super().__init__(
            parent = parent,
            click = ClickLambda(self, FonLeftClick = self.attemptToClick),
            drag = drag,
            drawOrder = drawOrder)

        self.center_px, self.center_py = center_px, center_py
        self.pwidth, self.pheight = pwidth, pheight

        self.states: dict[Enum, ImageState] = {}
        self.defaultID = None
        if isinstance(states, ImageState):
            self.addState(states)
        else:
            [self.addState(state) for state in states]

        self.getStateID = getStateID
        
        self.dimOnHover = dimOnHover
        self.onClick = onClick
        self.isOn = isOn

        self.recomputePosition()

    def addState(self, state: ImageState):
        self.states[state.id] = state
        if self.defaultID is None:
            self.defaultID = state.id

    def getCurrentState(self) -> ImageState:
        id = self.getStateID()
        if id is None:
            id = self.defaultID
        elif id not in self.states:
                raise Exception("State not found")  

        return self.states[id]

    def setState(self, id):
        if id not in self.states:
            raise Exception("State not found")
        self.currentID = id

    def attemptToClick(self, mouse: tuple):
        if self.isOn():
            return self.onClick(mouse)
        return None

    def defineCenter(self) -> tuple:
        return self._px(self.center_px), self._py(self.center_py)
    
    def defineWidth(self) -> float:
        return self._pwidth(self.pwidth)
    
    def defineHeight(self) -> float:
        return self._pheight(self.pheight)

    # define the scaled image surfaces given the parent rect
    def defineOther(self) -> None:
        for state in self.states:
            self.states[state].update(self.images, self.WIDTH, self.HEIGHT)       

    def getTooltip(self) -> Tooltip | None:
        return self.getCurrentState().getTooltip(self.isOn())

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        image = self.getCurrentState().getSurface(self.isOn(), isHovered and self.dimOnHover)

        if self.getOpacity() != 1:
            image.set_alpha(self.getOpacity() * 255)

        drawSurface(screen, image, self.CENTER_X, self.CENTER_Y)
            