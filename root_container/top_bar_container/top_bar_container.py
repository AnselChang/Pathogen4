from entity_base.container_entity import Container
import entity_base.entity as entity
import pygame

class TopBarContainer(Container):

    def __init__(self):
        super().__init__(parent = entity.ROOT_CONTAINER)

        self.BACKGROUND_COLOR = (230, 230, 230)
    
    def defineTopLeft(self) -> tuple:
        return 0,0
    
    def defineWidth(self) -> float:
        return self.dimensions.TOP_WIDTH
    
    def defineHeight(self) -> float:
        return self.dimensions.TOP_HEIGHT

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, self.RECT)