from __future__ import annotations
from typing import TYPE_CHECKING

from root_container.top_bar_container.project_name import ProjectName

if TYPE_CHECKING:
    from models.project_model import ProjectModel

from entity_base.container_entity import Container
import entity_base.entity as entity
import pygame

class TopBarContainer(Container):

    def __init__(self, model: ProjectModel):
        super().__init__(parent = entity.ROOT_CONTAINER)

        self.BACKGROUND_COLOR = (220, 220, 220)
        self.model = model

        self.projectName = ProjectName(self, model)
    
    def defineTopLeft(self) -> tuple:
        return 0,0
    
    def defineWidth(self) -> float:
        return self.dimensions.TOP_WIDTH
    
    def defineHeight(self) -> float:
        return self.dimensions.TOP_HEIGHT

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, self.RECT)