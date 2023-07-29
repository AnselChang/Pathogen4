from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID

from data_structures.observer import Observer
from entity_base.aligned_entity_mixin import HorizontalAlign, VerticalAlign
from entity_base.container_entity import Container
from views.text_view.text_view import TextView
from views.text_view.text_view_config import TextConfig, TextReplacement, VisualConfig, VisualConfigState
from models.project_model import ProjectModel

if TYPE_CHECKING:
    
    from entities.root_container.top_bar_container.top_bar_container import TopBarContainer


class ProjectName(Container):

    def __init__(self, parent: TopBarContainer):
        super().__init__(parent)

        self.model = ProjectModel.getInstance()

        textConfig = TextConfig(TextReplacement.CPP,
                                HorizontalAlign.LEFT,
                                VerticalAlign.CENTER,
                                TextConfig.RE_ALPHANUMERIC_SPACE,
                                TextConfig.RE_ALPHANUMERIC_SPACE,
                                0, True, # flexible width
                                1, False # static height of 3
                                )
        
        stateI = VisualConfigState((0,0,0), parent.BACKGROUND_COLOR)
        stateH = VisualConfigState((0,0,0), (210, 210, 210))
        stateAV = VisualConfigState((0,0,0), (200, 200, 200), 1, (0,0,0))
        stateAI = VisualConfigState((0,0,0), (200, 200, 200), 1, (255,0,0))
        visualConfig = VisualConfig(stateI, stateH, stateAV, stateAI,
                                    FontID.FONT_TITLE, 18,
                                    radius = 3)

        self.view = TextView(self, self.model.getData().projectName, textConfig, visualConfig)


    def defineLeftX(self) -> float:
        return self._ax(30)