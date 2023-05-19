from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from adapter.path_adapter import NullPathAdapter
from command_creation.command_definition_database import CommandDefinitionDatabase

from data_structures.linked_list import LinkedList
from typing import TypeVar, Generic

from entity_base.entity import Entity
from models.command_models.buildable_from_command_model import BuildableFromCommandModel
from root_container.panel_container.command_block.command_inserter import CommandInserter

if TYPE_CHECKING:
    from models.command_models.command_model import CommandModel

"""
Interface for something that has a CommandElement parent, and that
has 0 or more command children.
CommandSections have a parent of None
Command blocks usualy have a parent of sections, or tasks/loops if they're inside them
"""

T1 = TypeVar('T1') # parent type
T2 = TypeVar('T2') # children type
class AbstractModel(Generic[T1, T2]):
    def __init__(self, parent: AbstractModel | T1 = None):
        
        self.parent = parent
        self.children = LinkedList[AbstractModel | T2]()

        self.ui = None

    def insertChildAfter(self, child: AbstractModel | T2, after: AbstractModel | T2):
        self.children.insertAfter(after, child)

    def insertChildAtBeginning(self, child: AbstractModel | T2):
        self.children.addToBeginning(child)

    def insertChildAtEnd(self, child: AbstractModel | T2):
        self.children.addToEnd(child)

    def onInserterClicked(self, elementBeforeInserter: AbstractModel):
        commandModel = self.createCustomCommandModel()

        if elementBeforeInserter is None:
            self.insertChildAtBeginning(commandModel)
        else:
            self.insertChildAfter(commandModel, elementBeforeInserter)

    def canHaveChildren(self) -> bool:
        raise NotImplementedError
    
    def createChild(self) -> AbstractModel | T2:

        if not self.canHaveChildren():
            raise Exception("Cannot create child for this model")

        raise NotImplementedError
    
    def createCustomCommandModel(self) -> CommandModel:
        return CommandModel(NullPathAdapter())
    
    def createInserterUI(self, elementBeforeInserter: AbstractModel) -> CommandInserter:
        return CommandInserter(None, lambda: self.onInserterClicked(elementBeforeInserter), elementBeforeInserter is None)

    # implement this to generate the UI for this element ONLY (not children)
    def generateUIForMyself(self, parent: Entity) -> BuildableFromCommandModel | Entity:
        raise NotImplementedError
    
    # return cached UI for this element
    def getExistingUI(self) -> BuildableFromCommandModel | Entity:
        assert(self.ui is not None)
        return self.ui
    
    # rebuild the UI for this element
    # If rebuildChildren, rebuilds children as well.
    # Otherwise, links the already-computed UI for children to this element
    def rebuild(self, parentUI: Entity, rebuildChildren: bool = False) -> None:
        self.ui = self.generateUIForMyself(parentUI)

        if not self.canHaveChildren():
            return

        # clear existing child ui before re-adding all
        self.ui.clearChildUI()

        # add first inserter UI
        self.ui.addChildUI(self.createInserterUI(None))

        for child in self.children:

            if rebuildChildren:
                childUI = child.rebuild(self.ui, True)
            else:
                childUI = child.getExistingUI()

            # add the section/command UI
            self.ui.addChildUI(childUI)

            # add the inserter UI
            self.ui.addChildUI(self.createInserterUI(child))