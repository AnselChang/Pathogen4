from common.image_manager import ImageID
from data_structures.variable import Variable
from entity_base.aligned_entity_mixin import AlignedEntityMixin, HorizontalAlign, VerticalAlign
from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.hover_listener import HoverLambda
from utility.pygame_functions import brightenSurface, scaleImageToRect
from views.view import View
import pygame

"""
Describes a view that manipulates a boolean variable through a checkbox.
By default, size is the largest square that fits in parent rect.
But, can pass in pixel size
"""
class CheckboxView(AlignedEntityMixin, Entity, View):

    def __init__(self, parent: Entity,
                isOn: Variable[bool], # variable must be boolean
                sizePixels: float = None, # size of checkbox. defaults to parent rect,
                horizontalAlign: HorizontalAlign = HorizontalAlign.CENTER,
                verticalAlign: VerticalAlign = VerticalAlign.CENTER
            ):
        
        self.isOn = isOn
        self.isOn.subscribe(self, onNotify = self.recomputeEntity)

        self.sizePixels = sizePixels

        # assert isOn variable is boolean
        assert(isinstance(self.isOn.get(), bool))

        Entity.__init__(self, parent,
            hover = HoverLambda(self,
                FonHoverOn = self.recomputeEntity,
                FonHoverOff = self.recomputeEntity
            ),
            click = ClickLambda(self, FonLeftClick = self.onClick)
        )

        super().__init__(horizontalAlign, verticalAlign)

    # get the value the checkbox is derived from
    def getValue(self) -> bool:
        return self.isOn.get()
    
    # set a new value for the variable
    def setValue(self, value: bool):
        self.isOn.set(value)

    # toggle checkbox
    # calling recompute not necessary as setValue will already do so through notif
    def onClick(self, mouse: tuple):
        self.setValue(not self.getValue())

    # determine size of checkbox (square)
    def defineBefore(self) -> None:
        if self.sizePixels is None:
            # largest square that fits inside parent rect
            self.SIZE = min(self._pwidth(1), self._pheight(1))
        else:
            # scale specified pixel size into current resolution
            self.SIZE = self._awidth(self.sizePixels)

        iconID = ImageID.CHECKBOX_ON if self.getValue() else ImageID.CHECKBOX_OFF
        self.ICON = scaleImageToRect(self.images.get(iconID), self.SIZE, self.SIZE)
        if self.hover.isHovering:
            self.ICON = brightenSurface(self.ICON, 60)

    def defineWidth(self) -> float:
        return self.SIZE
    def defineHeight(self) -> float:
        return self.SIZE
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        screen.blit(self.ICON, [self.LEFT_X, self.TOP_Y])