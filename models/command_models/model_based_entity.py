from __future__ import annotations
from typing import TYPE_CHECKING

from root_container.panel_container.command_block.inserter_interface import ICommandInserter

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
    
    class InserterData:
        def __init__(self, inserter: CommandInserter, before: CommandBlockEntity = None, after: CommandBlockEntity = None):
            self.inserter = inserter
            self.before = before
            self.after = after

        def __repr__(self) -> str:
            idi = id(self.inserter)
            idb = 0 if self.before is None else id(self.before)
            ida = 0 if self.after is None else id(self.after)
            return f"{idi} {idb} {ida}"

    # return an ordered list of inserters+ from top to bottom
    # exclude section inserters
    # exclude inserters inside collapsed sections/tasks
    # package with references to commands before and after inserter
    def flatten(self) -> list[InserterData]:
        inserters: list[FullContainer.InserterData] = []
        self._flatten(inserters)
        return inserters

    def _flatten(self, inserters: list[FullContainer.InserterData]) -> list[InserterData]:

        if self.getChildVGC() is None:
            return

        children: list[VariableContainer] = self.getChildVGC()._children
        for i in range(len(children)):
            
            before = children[i - 1].child if i > 0 else None
            entity = children[i].child
            after = children[i + 1].child if (i < len(children)-1) else None

            if isinstance(entity, ICommandInserter) and not self.model.isSectionModel():
                inserters.append(ModelBasedEntity.InserterData(entity, before, after))
            elif isinstance(entity, ModelBasedEntity):
                entity._flatten(inserters)