from enum import Enum

from utility.pygame_functions import brightenSurface, scaleImageToRect
from entity_ui.tooltip import Tooltip
from common.image_manager import ImageID, ImageManager
import pygame

# Images can be toggled between 1 or more states.
# At each state, the image can be off, on, and on + hovered.
class ImageState:

    def __init__(self, id: Enum, imageOnID: ImageID, tooltipOn = None, imageOffID: ImageID = None, tooltipOff = None, imageOnHoveredID: ImageID = None):
        self.id = id
        self.imageOffID = imageOffID
        self.imageOnID = imageOnID
        self.imageOnHoveredID = imageOnHoveredID

        self.tooltipOn = None if tooltipOn is None else Tooltip(tooltipOn)
        if tooltipOff is None:
            self.tooltipOff = self.tooltipOn
        else:
            self.tooltipOff = Tooltip(tooltipOff)

    def update(self, images: ImageManager, width, height):


        self.imageOn = scaleImageToRect(images.get(self.imageOnID), width, height)
        if self.imageOnHoveredID is None:
            self.imageOnH = brightenSurface(self.imageOn.copy(), 40) # brighten by 40 for hovered
        else:
            self.imageOnH = scaleImageToRect(images.get(self.imageOnHoveredID), width, height)

        if self.imageOffID is None:
            self.imageOff = brightenSurface(self.imageOn.copy(), 130) # brighten by 130 for disabled
        else:
            self.imageOff = scaleImageToRect(images.get(self.imageOffID), width, height)
        
    def getSurface(self, isOn: bool, isHovered: bool) -> pygame.Surface:
        if not isOn:
            return self.imageOff
        elif isHovered:
            return self.imageOnH
        else:
            return self.imageOn

    def getTooltip(self, isOn: bool) -> Tooltip | None:
        if isOn:
            return self.tooltipOn
        else:
            return self.tooltipOff
        
class ImageStatesFactory:

    def __init__(self):
        self.states: list[ImageState] = []

    def addState(self, id: Enum, imageOnID: ImageID, tooltipOn = None, imageOffID: ImageID = None, tooltipOff = None):
        state = ImageState(id, imageOnID, tooltipOn, imageOffID, tooltipOff)
        self.states.append(state)
        return state
    
    def create(self) -> list[ImageState]:
        return self.states