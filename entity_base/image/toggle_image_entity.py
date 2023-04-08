from common.reference_frame import PointRef
from entity_base.image.image_entity import ImageEntity
from entity_ui.tooltip import Tooltip

from utility.pygame_functions import brightenSurface
from common.draw_order import DrawOrder
from common.image_manager import ImageID
import pygame

"""
A generic image entity, where you pass in images
Is drawn to fit inside parent entity's rect
However, the additional feature compared to ImageEntity is that
it can toggle between two seperate images, depending on whether it is active
"""
class ToggleImageEntity(ImageEntity):

    # px, py, pwidth, pheight set by default to the dimensions of the parent
    # if imageOffID is None, then the image is set to dimmed when not on
    def __init__(self, parent, imageOnID: ImageID, imageOffID: ImageID,
                 drawOrder: DrawOrder, tooltip: str | list[str] = None,
                 onClick = lambda: None, isOn: bool = False, center_px = 0.5,
                 center_py = 0.5, pwidth = 1, pheight = 1, noHoveringIfOff: bool = False,
                 tooltipOff: str | list[str] = None
                 ):
        
        self.imageOffID = imageOffID
        self.isOn = isOn
        self.noHoveringIfOff = noHoveringIfOff

        if tooltipOff is None:
            self.tooltipOff = None
        else:
            self.tooltipOff = Tooltip(tooltipOff)
        
        super().__init__(parent, imageOnID, drawOrder, tooltip, onClick, center_px, center_py, pwidth, pheight)

        self.recomputePosition()

    # clickable only if on
    def attemptToClick(self, mouse: PointRef):
        if self.isOn():
            self.onClick(mouse)

    def getTooltip(self) -> Tooltip | None:

        if not self.isOn() and self.tooltipOff is not None:
            return self.tooltipOff

        return self.tooltip


    # define the scaled image surfaces given the parent rect
    def defineOther(self) -> None:

        super().defineOther()

        if self.imageOffID is None:
            imageOff = self.images.get(self.imageID)
            imageOff = pygame.transform.smoothscale(imageOff, (self.imageWidth, self.imageHeight))
            self.imageOffScaled = brightenSurface(imageOff, 130)
        else:
            imageOff = self.images.get(self.imageOffID)
            self.imageOffScaled = pygame.transform.smoothscale(imageOff, (self.imageWidth, self.imageHeight))
        
        self.imageOffScaledH = brightenSurface(self.imageOffScaled, self.HOVER_DELTA)

    
    def _getImage(self, isHovered):
        if self.isOn():
            return super()._getImage(isHovered)
        else:
            return self.imageOffScaledH if (isHovered and not self.noHoveringIfOff) else self.imageOffScaled