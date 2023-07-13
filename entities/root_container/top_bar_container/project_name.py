from __future__ import annotations
from typing import TYPE_CHECKING

from data_structures.observer import Observer
from entity_base.container_entity import Container

if TYPE_CHECKING:
    from models.project_model import ProjectModel
    from entities.root_container.top_bar_container.top_bar_container import TopBarContainer

from common.font_manager import FontID
from entity_ui.text.text_editor_entity import TextEditorEntity

class ProjectName(Container, Observer):

    def __init__(self, parent: TopBarContainer, model: ProjectModel):
        super().__init__(parent)

        self.model = model

        self.text = TextEditorEntity(parent = self,
            fontID = FontID.FONT_TITLE,
            fontSize = 18,
            isDynamic = False,
            isNumOnly = False,
            isCentered = False,
            isFixedWidth = False,
            defaultText = self.model.projectData.projectName.get(),
            hideTextbox = False,
            borderThicknessRead = 0,
            borderThicknessWrite = 2,
            readColor = parent.BACKGROUND_COLOR,
            readColorH = (210, 210, 210),
            maxTextLength = 17
        )

        self.text.subscribe(self, onNotify = self.onProjectNameUpdate)

    def onProjectNameUpdate(self):
        self.model.projectData.projectName.set(self.text.getText())

    def defineLeftX(self) -> float:
        return self._ax(30)
    
    def defineCenterY(self) -> float:
        return self._py(0.5)