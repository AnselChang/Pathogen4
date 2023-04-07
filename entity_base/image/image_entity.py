from common.reference_frame import PointRef, Ref
from entity_base.listeners.click_listener import ClickLambda
from entity_ui.group.radio_container import RadioContainer
from entity_base.entity import Entity

from utility.math_functions import isInsideBox2
from utility.pygame_functions import drawSurface, brightenSurface, scaleImageToRect
from common.dimensions import Dimensions
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
    def __init__(self, parent, imageID: ImageID, drawOrder: DrawOrder, tooltip: str | list[str] = None, onClick = lambda: None, center_px = 0.5, center_py = 0.5, pwidth = 1, pheight = 1, imageIDHovered: ImageID = None):
        super().__init__(
            parent = parent,
            click = ClickLambda(self, FonLeftClick = onClick),
            drawOrder = drawOrder)

        self.center_px, self.center_py = center_px, center_py
        self.pwidth, self.pheight = pwidth, pheight

        self.imageID = imageID
        self.imageIDHovered = imageIDHovered

        self.HOVER_DELTA = 50
        
        if tooltip is None:
            self.tooltip = None
        else:
            self.tooltip = Tooltip(tooltip)

        self.recomputePosition()

    # function doesn't make much sense for ToggleImageEntities.
    # Most obvious use case is command block icons
    def setImage(self, imageID: ImageID):
        self.imageID = imageID
        self.defineOther() # normally would have to recomputePosition(), but position doesn't change

    def defineCenter(self) -> tuple:
        return self._px(self.center_px), self._py(self.center_py)
    
    def defineWidth(self) -> float:
        return self._pwidth(self.pwidth)
    
    def defineHeight(self) -> float:
        return self._pheight(self.pheight)

    # define the scaled image surfaces given the parent rect
    def defineOther(self) -> None:
        self.imageScaled = scaleImageToRect(self.images.get(self.imageID), self.WIDTH, self.HEIGHT)
        
        self.imageWidth = self.imageScaled.get_width()
        self.imageHeight = self.imageScaled.get_height()
        
        if self.imageIDHovered is not None:
            self.imageScaledH = pygame.transform.smoothscale(self.images.get(self.imageIDHovered), (self.imageWidth, self.imageHeight))
        else:
            self.imageScaledH = brightenSurface(self.imageScaled, self.HOVER_DELTA)

        

    def getTooltip(self) -> Tooltip | None:
        return self.tooltip
    
    def _getImage(self, isHovered):
        return self.imageScaledH if isHovered else self.imageScaled

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        drawSurface(screen, self._getImage(isHovered), self.CENTER_X, self.CENTER_Y)
            