from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

from data_structures.linked_list import LinkedList, LinkedListNode
from typing import TypeVar, Generic

from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter


"""
A single-source-of-truth model storing the internal state of some
recursive element, like a command block or a section. It handles
the recursive generation of UI elements from the model for itself and its children,
and has the option to regenerate the UI for itself without needing
to regenerate the UI for its children through caching.
"""

T1 = TypeVar('T1') # parent type
T2 = TypeVar('T2') # children type
class AbstractModel(LinkedListNode['AbstractModel'], Generic[T1, T2]):

    def __init__(self, name: str = "AbstractModel"):

        super().__init__()

        self.name = name
        
        self.parent: 'AbstractModel' = None
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
        return self.children.head
    
    def getLastChild(self) -> AbstractModel | T2:
        return self.children.tail
    
    # insert a sibling model after this model
    def insertAfterThis(self, model: AbstractModel | T2) -> None:
        self.parent.insertChildAfter(model, self)
        self.parent.rebuild(rebuildChildren = False)

    # insert a sibling model before this model
    def insertBeforeThis(self, model: AbstractModel | T2) -> None:
        if self._prev is None:
            self.parent.insertChildAtBeginning(model)
        else:
            self.parent.insertChildAfter(model, self._prev)
        self.parent.rebuild(rebuildChildren = False)

    def insertChildAfter(self, child: AbstractModel | T2, after: AbstractModel | T2):
        child.parent = self
        self.children.insertAfter(after, child)
        self.rebuild(rebuildChildren = False)

    def insertChildAtBeginning(self, child: AbstractModel | T2):
        child.parent = self
        self.children.addToBeginning(child)
        self.rebuild(rebuildChildren = False)

    def insertChildAtEnd(self, child: AbstractModel | T2):
        child.parent = self
        self.children.addToEnd(child)
        self.rebuild(rebuildChildren = False)

    def onInserterClicked(self, elementBeforeInserter: AbstractModel):

        print("Inserter clicked")

        sectionOrCommand = self._createChild()

        if elementBeforeInserter is None:
            self.insertChildAtBeginning(sectionOrCommand)
        else:
            self.insertChildAfter(sectionOrCommand, elementBeforeInserter)

        self.rebuild(rebuildChildren = False)
        self.ui.propagateChange()
    
    def createInserterUI(self, elementBeforeInserter: AbstractModel) -> CommandInserter:
        return CommandInserter(self.getParentUI(), lambda: self.onInserterClicked(elementBeforeInserter), elementBeforeInserter is None)

    
    # return cached UI for this element
    def getExistingUI(self) -> ModelBasedEntity | Entity:
        assert(self.ui is not None)
        return self.ui
    
    # Delete this model
    def delete(self) -> None:
        if self.parent is not None:
            self.parent.children.remove(self)
            self.parent.rebuild(False)
        else:
            raise Exception("Cannot delete root model")
    

    def getParentUI(self) -> Entity:

        if self.parent is None:
            raise NotImplementedError("FullModel must implement getParentUI differently")

        return self.parent.getExistingUI()
    
    # rebuild the UI for this element
    # If rebuildChildren, rebuilds children as well.
    # Otherwise, links the already-computed UI for children to this element
    def rebuild(self, rebuildChildren: bool = False, isRoot: bool = True) -> None:
        self.ui = self._generateUIForMyself()
        assert(isinstance(self.ui, ModelBasedEntity) and isinstance(self.ui, Entity))

        if not self._canHaveChildren():
            return
        
        # add first inserter UI
        self.ui.addChildUI(self.createInserterUI(None))

        for child in self.children:

            if rebuildChildren or child.ui is None:
                child.rebuild(True, False)
            
            # add the section/command UI
            self.ui.addChildUI(child.getExistingUI())

            # add the inserter UI
            self.ui.addChildUI(self.createInserterUI(child))

        if isRoot:
            pass
            #self.ui.recomputeEntity()

    # print this element and all children as tree structure for debugging
    def tree(self, indent: int = 0):
        print(" " * indent + self.name)
        for child in self.children:
            child.tree(indent + 2)