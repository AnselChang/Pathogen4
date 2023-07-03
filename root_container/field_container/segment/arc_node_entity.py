from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.listeners.drag_listener import DragLambda
from utility.math_functions import distancePointToLine
if TYPE_CHECKING:
    from root_container.field_container.segment.arc_segment_entity import ArcSegmentEntity

from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda

import pygame
from utility.pygame_functions import shade

class ArcNodeEntity(Entity):

    def __init__(self, segment: ArcSegmentEntity):

        super().__init__(parent = segment,
            hover = HoverLambda(self),
            drag = DragLambda(self, selectEntityNotThis = segment, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FonStopDrag = self.onStopDrag),
        )

        self.field = segment.field
        self.segment = segment

        self.COLOR = [255, 128, 0]
        self.COLOR_H = shade(self.COLOR, 0.9)

        self.RADIUS = 5
        self.RADIUS_H = 6

    def _findPerpDistance(self, mouse: tuple) -> float:
        beforePos = self.segment.beforePos
        afterPos = self.segment.afterPos

        perpPixels = -distancePointToLine(*mouse, *beforePos, *afterPos, True)
        return self.field.scalarMouseToInches(perpPixels)

    def onStartDrag(self, mouse: tuple):
        startPerp = self._findPerpDistance(mouse)
        currentPerp = self.segment.getArcState().getPerpDistance()

        self.perpOffset = currentPerp - startPerp

    def onDrag(self, mouse: tuple):
        rawPerp = self._findPerpDistance(mouse)
        adjustedPerp = rawPerp# - self.perpOffset
        self.segment.getArcState().setPerpDistance(adjustedPerp)

    def onStopDrag(self):
        pass

    def defineCenter(self) -> tuple:
        centerInches = self.segment.getArcState().getArcMidpoint()
        print("centerInches", centerInches)
        return self.field.inchesToMouse(centerInches)
    
    def isTouching(self, position: tuple) -> bool:
        MARGIN = 4
        return self.distanceTo(position) <= self.RADIUS + MARGIN
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        RADIUS = self.RADIUS_H if self.hover.isHovering else self.RADIUS
        COLOR = self.COLOR_H if self.hover.isHovering else self.COLOR
        POSITION = [self.CENTER_X, self.CENTER_Y]
        pygame.draw.circle(screen, COLOR, POSITION, RADIUS)