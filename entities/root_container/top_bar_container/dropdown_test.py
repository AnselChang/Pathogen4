from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID

from data_structures.observer import Observer
from entity_base.aligned_entity_mixin import HorizontalAlign, VerticalAlign
from entity_base.container_entity import Container
from models.ui_model import UIModel
from views.dropdown_view.dropdown_view import DropdownView
from views.dropdown_view.dropdown_view_config import DropdownConfig

if TYPE_CHECKING:
    from models.project_model import ProjectModel
    from entities.root_container.top_bar_container.top_bar_container import TopBarContainer


class DropdownTest(Container):

    def __init__(self, parent: TopBarContainer):
        super().__init__(parent)

        self.model = UIModel.getInstance()

        config = DropdownConfig(HorizontalAlign.CENTER,
                                FontID.FONT_CODE, 10,
                                )
        
        self.view = DropdownView(self,
                                 self.model.testActiveOption,
                                 self.model.testAllOptions,
                                 config
                                 )

    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        self.drawRect(screen)