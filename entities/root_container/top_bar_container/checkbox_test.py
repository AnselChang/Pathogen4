from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID

from data_structures.observer import Observer
from entity_base.aligned_entity_mixin import HorizontalAlign, VerticalAlign
from entity_base.container_entity import Container
from models.ui_model import UIModel
from views.checkbox_view.checkbox_view import CheckboxView
from views.text_view.text_view import TextView
from views.text_view.text_view_config import TextConfig, TextReplacement, VisualConfig, VisualConfigState

if TYPE_CHECKING:
    from models.project_model import ProjectModel
    from entities.root_container.top_bar_container.top_bar_container import TopBarContainer


class CheckboxTest(Container):

    def __init__(self, parent: TopBarContainer):
        super().__init__(parent)

        self.model = UIModel.getInstance()

        self.checkbox = CheckboxView(self, self.model.testBool, 25)

    def defineCenterX(self) -> float:
        return self._px(0.9)