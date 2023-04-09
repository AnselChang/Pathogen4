from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.selector_menu.selector_menu_entity import SelectorMenuEntity

from common.draw_order import DrawOrder
from entity_base.entity import Entity
from utility.math_functions import distance
from utility.bezier_functions import bezier_curve_points
import math, pygame

"""
Handles drawing the line between the menu and the selected entity
# Finds closest corner on menu, and uses a bezier curve through three points
Is drawn below everything else on the field
"""

class MenuLineEntity(Entity):

    def __init__(self, menuBackground: SelectorMenuEntity, entity: Entity):

        super().__init__(parent = menuBackground, drawOrder = DrawOrder.MENU_LINE)

        self.menu = menuBackground
        self.entity = entity

        self.COLOR = [50]*3

        self.recomputePosition()

    # Draws the background of the menu
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):

        # draw an arc from menu to entity
        pygame.draw.aalines(screen, self.COLOR, False, self.points)
        #pygame.draw.circle(screen, (0,255,0), self.p2, 3)

    # position is defined to be identical to parent menu

    # calculate bezier curve
    def defineOther(self):
        # first and third point is the closest corner on the menu to the entity
        # second point is the closest corner plus delta in that direction
        ep = [self.entity.CENTER_X, self.entity.CENTER_Y]
        closest = math.inf
        
        # iterate through four corners to find closest to entity
        for corner in [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]:
            x = self.CENTER_X + corner[0] * self.WIDTH/2
            y = self.CENTER_Y + corner[1] * self.HEIGHT/2
            DELTA = distance(x, y, *ep) * 0.5 # distance from menu corner to intermediate point
            dist = distance(x, y, *ep)
            if dist < closest:
                closest = dist
                x1 = x
                y1 = y
                xm = x + corner[0] * DELTA
                ym = y + corner[1] * DELTA

                midA = (x1, ym)
                midB = (xm, y1)

                # pick the intermediate point closer to entity
                if distance(*midA, *ep) < distance(*midB, *ep):
                    x2, y2 = midA
                else:
                    x2, y2 = midB
        
        # generate bezier from three points
        self.p1 = (x1,y1)
        self.p2 = (x2, y2)
        self.p3 = (self.entity.CENTER_X, self.entity.CENTER_Y)
        self.points = bezier_curve_points(self.p1, self.p2, self.p3, 2)
