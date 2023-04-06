from entity_base.image.image_entity import ImageEntity

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
    def __init__(self, parent, imageOnID: ImageID, imageOffID: ImageID, drawOrder: DrawOrder, tooltip: str | list[str] = None, onClick = lambda: None, isOn: bool = False, center_px = 0.5, center_py = 0.5, pwidth = 1, pheight = 1):
        
        super().__init__(parent, imageOnID, drawOrder, tooltip, onClick, center_px, center_py, pwidth, pheight)

        self.imageOffID = imageOffID
        self.isOn = isOn


    # define the scaled image surfaces given the parent rect
    def defineOther(self) -> None:

        super().defineOther()

        self.imageOffScaled = pygame.transform.smoothscale(self.images.get(self.imageOffID), self.imageWidth, self.imageHeight)
        self.imageOffScaledH = brightenSurface(self.imageOffScaled, self.HOVER_DELTA)

    
    def _getImage(self, isHovered):
        if self.isOn():
            return super()._getImage(isHovered)
        else:
            return self.imageOffScaledH if isHovered else self.imageOffScaled