from entity_base.container_entity import Container
from entity_base.entity import Entity
import pygame

"""
A class that takes leftx, topy, in awidth, aheight within parent rect
Also takes in color and border radius
Draws panel background
"""

class PanelContainer(Entity):
    
    def __init__(self, parent,
        px: float,
        py: float,
        pw: float,
        ph: float,
        padding: float = 0,
        color: tuple = None,
        radius: float = 0
    ):
        self.px = px
        self.py = py
        self.pw = pw
        self.ph = ph
        self.padding = padding
        self.color = color
        self.radius = radius

        super().__init__(parent)

    def defineBefore(self) -> None:
        self.p = self._awidth(self.padding)

    def defineTopLeft(self) -> tuple:
        return self._px(self.px) + self.p, self._py(self.py) + self.p
    
    def defineWidth(self) -> float:
        return self._pwidth(self.pw) - self.p*2
    
    def defineHeight(self) -> float:
        return self._pheight(self.ph) - self.p*2

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        if self.color is not None:
            pygame.draw.rect(screen, self.color, self.RECT, border_radius = self.radius)