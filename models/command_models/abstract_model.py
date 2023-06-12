from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from adapter.path_adapter import NullPathAdapter
from command_creation.command_definition_database import CommandDefinitionDatabase

from data_structures.linked_list import LinkedList, LinkedListNode
from typing import TypeVar, Generic

from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
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
class AbstractModel(LinkedListNode['AbstractModel'], Generic[T1, T2]):

    def __init__(self, name: str = "AbstractModel"):

        super().__init__()

        self.name = name
        
        self.parent = None
        self.children = LinkedList[AbstractModel | T2]()

        self.ui = None

    # must be implemented by subclasses
    def _canHaveChildren(self) -> bool:
        raise NotImplementedError
    
    # must be implemented by subclasses
    def _createChild(self) -> AbstractModel | T2:

        if not self._canHaveChildren():
            raise Exception("Cannot create child for this model")

        raise NotImplementedError
    
    # must be implemented by subclasses
    # implement this to generate the UI for this element ONLY (not children)
    def _generateUIForMyself(self) -> ModelBasedEntity | Entity:
        raise NotImplementedError(self)
    
    def getFirstChild(self) -> AbstractModel | T2:
        return self.children[0]

    def insertChildAfter(self, child: AbstractModel | T2, after: AbstractModel | T2):
        child.parent = self
        self.children.insertAfter(after, child)

    def insertChildAtBeginning(self, child: AbstractModel | T2):
        child.parent = self
        self.children.addToBeginning(child)

    def insertChildAtEnd(self, child: AbstractModel | T2):
        child.parent = self
        self.children.addToEnd(child)

    def onInserterClicked(self, elementBeforeInserter: AbstractModel):
        sectionOrCommand = self._createChild()

        if elementBeforeInserter is None:
            self.insertChildAtBeginning(sectionOrCommand)
        else:
            self.insertChildAfter(sectionOrCommand, elementBeforeInserter)
    
    def createCustomCommandModel(self) -> CommandModel:
        return CommandModel(NullPathAdapter())
    
    def createInserterUI(self, elementBeforeInserter: AbstractModel) -> CommandInserter:
        return CommandInserter(None, lambda: self.onInserterClicked(elementBeforeInserter), elementBeforeInserter is None)

    
    # return cached UI for this element
    def getExistingUI(self) -> ModelBasedEntity | Entity:
        assert(self.ui is not None)
        return self.ui
    
    # Delete this model
    def delete(self) -> None:
        if self.parent is not None:
            self.parent.children.remove(self)
        else:
            raise Exception("Cannot delete root model")
    

    def getParentUI(self) -> Entity:

        if self.parent is None:
            raise NotImplementedError("FullModel must implement getParentUI differently")

        return self.parent.getExistingUI()
    
    # rebuild the UI for this element
    # If rebuildChildren, rebuilds children as well.
    # Otherwise, links the already-computed UI for children to this element
    def rebuild(self, rebuildChildren: bool = False) -> None:
        self.ui = self._generateUIForMyself()
        assert(isinstance(self.ui, ModelBasedEntity))

        if not self._canHaveChildren():
            return
        
        # add first inserter UI
        self.ui.addChildUI(self.createInserterUI(None))

        for child in self.children:

            if rebuildChildren:
                child.rebuild(True)
            
            # add the section/command UI
            self.ui.addChildUI(child.getExistingUI())

            # add the inserter UI
            self.ui.addChildUI(self.createInserterUI(child))

    # print this element and all children as tree structure for debugging
    def tree(self, indent: int = 0):
        print(" " * indent + self.name)
        for child in self.children:
            child.tree(indent + 2)