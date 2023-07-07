from __future__ import annotations
from typing import TYPE_CHECKING
from common.image_manager import ImageID
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
from root_container.top_bar_container.command_editor_button import CommandEditorButtonDefinition

from root_container.top_bar_container.project_name import ProjectName
from root_container.top_bar_container.top_bar_button_container import ButtonDefinition, SimpleButtonDefinition, TopBarButtonContainer

if TYPE_CHECKING:
    from models.project_model import ProjectModel

from entity_base.container_entity import Container
import entity_base.entity as entity
import pygame


class TopBarContainer(Container):

    def __init__(self, model: ProjectModel):
        super().__init__(parent = entity.ROOT_CONTAINER)

        self.BACKGROUND_COLOR = entity.ROOT_CONTAINER.BACKGROUND_COLOR
        self.model = model

        self.projectName = ProjectName(self, model)

        undo = SimpleButtonDefinition(ImageID.UNDO, self.onUndo, "Undo")
        redo = SimpleButtonDefinition(ImageID.REDO, self.onRedo, "Redo")
        TopBarButtonContainer(self, 0.3, [undo, redo], 10)
        undo = SimpleButtonDefinition(ImageID.UNDO, self.onUndo, "Undo")
        redo = SimpleButtonDefinition(ImageID.REDO, self.onRedo, "Redo")
        TopBarButtonContainer(self, 0.8, [undo, redo], 20)

        # button for toggling command editor
        TopBarButtonContainer(self, 0.4, CommandEditorButtonDefinition(), 20)


    def onUndo(self, mouse):
        print("undo")

    def onRedo(self, mouse):
        print("redo")
    
    def defineTopLeft(self) -> tuple:
        return 0,0
    
    def defineWidth(self) -> float:
        return self.dimensions.TOP_WIDTH
    
    def defineHeight(self) -> float:
        return self.dimensions.TOP_HEIGHT

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass
        #pygame.draw.rect(screen, self.BACKGROUND_COLOR, self.RECT)