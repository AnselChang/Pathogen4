from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
from models.command_models.model_based_entity import ModelBasedEntity

if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
    from root_container.panel_container.command_block.command_inserter import CommandInserter
    from entity_ui.group.variable_group.variable_container import VariableContainer

class FullContainer(Container, ModelBasedEntity):
    
    def __init__(self, parent: Entity, model: ModelBasedEntity):
        super().__init__(parent = parent)
        ModelBasedEntity.__init__(self, model)

        self.vgc = VariableGroupContainer(self,
            isHorizontal = False,
            innerMargin = 1,
            outerMargin = 5
            )

    def onAddChild(self, child: Entity):
        if not isinstance(child, VariableGroupContainer):
            raise Exception("FullContainer should non-VGC added to it", child)

    def getChildVGC(self) -> VariableGroupContainer:
        return self.vgc

    def defineWidth(self) -> float:
        return self._mwidth(4)
    
    def defineHeight(self) -> float:
        return self._pheight(1)
    
    def defineCenterX(self) -> float:
        return self._px(0.5)
    
    def defineTopY(self) -> float:
        return self._py(0)