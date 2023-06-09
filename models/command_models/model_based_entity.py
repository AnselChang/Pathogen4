from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.command_models.abstract_model import AbstractModel
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
    from root_container.panel_container.command_block.full_container import FullContainer
    from root_container.panel_container.command_block.command_inserter import CommandInserter

from entity_base.entity import Entity
from entity_ui.group.variable_group.variable_container import VariableContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer

"""
This class represents a UI element that can be generated on 1:1 correlation
from a model. It contains code to interface between model and ui.
"""

class ModelBasedEntity:

    def __init__(self, model: AbstractModel):
        self.model = model

    def getRootEntity(self) -> FullContainer:
        return self.model.getRootModel().getExistingUI()

    def clearChildUI(self) -> None:
        self.getChildVGC().clear()

    # add a child UI element to this UI element
    def addChildUI(self, childUI: Entity) -> None:

        assert(childUI is not None)

        vc = VariableContainer(self.getChildVGC(), False)
        vc.setChild(childUI)
        childUI.changeParent(vc)
    
    # Implement this in entity subclasses as an endpoint for this class
    # and model to interface with the children of this ui element
    def getChildVGC(self) -> VariableGroupContainer:
        raise NotImplementedError