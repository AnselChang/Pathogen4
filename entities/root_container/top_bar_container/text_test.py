from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID

from data_structures.observer import Observer
from entity_base.aligned_entity_mixin import HorizontalAlign, VerticalAlign
from entity_base.container_entity import Container
from models.ui_model import UIModel
from views.text_view.text_view import TextView
from views.text_view.text_view_config import TextConfig, TextReplacement, VisualConfig, VisualConfigState

if TYPE_CHECKING:
    from models.project_model import ProjectModel
    from entities.root_container.top_bar_container.top_bar_container import TopBarContainer


class TextTest(Container):

    def __init__(self, parent: TopBarContainer):
        super().__init__(parent)

        self.model = UIModel.getInstance()

        textConfig = TextConfig(TextReplacement.CPP,
                                HorizontalAlign.CENTER,
                                VerticalAlign.CENTER,
                                TextConfig.RE_ANY,
                                TextConfig.RE_INTEGER,
                                0, True, # flexible width
                                3, False # static height of 3
                                )
        
        stateI = VisualConfigState((0,0,0), (235,235,235))
        stateH = VisualConfigState((0,0,0), (245,245,245))
        stateAV = VisualConfigState((0,0,0), (245,245,255), 1, (0,0,0))
        stateAI = VisualConfigState((0,0,0), (245,245,255), 1, (255,0,0))
        visualConfig = VisualConfig(stateI, stateH, stateAV, stateAI,
                                    FontID.FONT_CODE, 14,
                                    radius = 3)

        self.view = TextView(self, self.model.testVar, textConfig, visualConfig)


    def defineCenter(self) -> float:
        return self._px(0.5), self._py(0.5)