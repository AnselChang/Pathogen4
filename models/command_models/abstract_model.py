from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

from data_structures.linked_list import LinkedList, LinkedListNode
from typing import TypeVar, Generic

from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter


if TYPE_CHECKING:
    from entity_ui.group.variable_group.variable_container import VariableContainer


"""
A single-source-of-truth model storing the internal state of some
recursive element, like a command block or a section. It handles
the recursive generation of UI elements from the model for itself and its children,
and has the option to regenerate the UI for itself without needing
to regenerate the UI for its children through caching.
"""

T1 = TypeVar('T1') # parent type
T2 = TypeVar('T2') # children type
class AbstractModel(Generic[T1, T2]):

    def __init__(self, name: str = "AbstractModel"):

        super().__init__()

        self.name = name
        
        self.parent: 'AbstractModel' = None
        self.children: list[AbstractModel | T2] = []

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
        return None if len(self.children) == 0 else self.children[0]
    
    def getLastChild(self) -> AbstractModel | T2:
        return None if len(self.children) == 0 else self.children[-1]
    
    def getIndex(self, child: AbstractModel):
        return self.children.index(child)
    
    # insert a sibling model after this model
    def insertAfterThis(self, model: AbstractModel | T2) -> None:
        self.parent.insertChildAfter(model, self)
        self.parent.rebuild()

    # insert a sibling model before this model
    def insertBeforeThis(self, model: AbstractModel | T2) -> None:

        i = self.parent.getIndex(self)

        if i == 0:
            self.parent.insertChildAtBeginning(model)
        else:
            self.parent.insertChildAfter(model, self.parent.children[i-1])
        self.parent.rebuild()

    def insertChildAfter(self, child: AbstractModel | T2, after: AbstractModel | T2):
        child.parent = self

        i = self.getIndex(after)
        self.children.insert(i+1, child)
        self.rebuild()

    def insertChildAtBeginning(self, child: AbstractModel | T2):
        child.parent = self
        self.children.insert(0, child)
        self.rebuild()

    def insertChildAtEnd(self, child: AbstractModel | T2):
        child.parent = self
        self.children.append(child)
        self.rebuild()

    def onInserterClicked(self, elementBeforeInserter: AbstractModel):

        print("Inserter clicked")

        sectionOrCommand = self._createChild()

        if elementBeforeInserter is None:
            self.insertChildAtBeginning(sectionOrCommand)
        else:
            self.insertChildAfter(sectionOrCommand, elementBeforeInserter)

        self.rebuild()
        self.ui.recomputeEntity()
    
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
            self.parent.rebuild()
        else:
            raise Exception("Cannot delete root model")
    

    def getParentUI(self) -> Entity | ModelBasedEntity:

        if self.parent is None:
            raise NotImplementedError("FullModel must implement getParentUI differently")

        return self.parent.getExistingUI()
    
    def getParentVGC(self) -> Entity:
        return self.getParentUI().getChildVGC()
    
    # reassign the UI for this element, making sure parent's child reference is correctly updated
    def reassignSelfUI(self, newUI: ModelBasedEntity | Entity) -> None:

        # if this is the root model, do nothing
        if self.parent is None:
            if self.ui is not None:
                self.ui.entities.removeEntity(self.ui)
            self.ui = newUI
            return
        
        # search for the child reference in the parent
        for childVC in self.parent.ui.getChildVGC()._children:

            childVC: VariableContainer = childVC

            if childVC.child is self.ui:
                childVC.setChild(newUI)
                childVC.removeChild(self.ui)
                newUI.changeParent(childVC)
                break

        if self.ui is not None:
            self.ui.entities.removeEntity(self.ui)
        
        self.ui = newUI
    
    # rebuild the UI for this element
    # If rebuildChildren, rebuilds children as well.
    # Otherwise, links the already-computed UI for children to this element
    def rebuild(self, isRoot: bool = True) -> None:

        if isRoot:
            print("rebulding", self)
        
        self.reassignSelfUI( self._generateUIForMyself() )
        
        if not isinstance(self.ui, ModelBasedEntity) and isinstance(self.ui, Entity):
            raise Exception("Model must generate ModelBasedEntity", self.ui)

        if not self._canHaveChildren():
            return
                
        # add first inserter UI
        self.ui.addChildUI(self.createInserterUI(None))

        for child in self.children:

            child.rebuild(False)
            
            # add the section/command UI
            self.ui.addChildUI(child.getExistingUI())

            # add the inserter UI
            self.ui.addChildUI(self.createInserterUI(child))


    # print this element and all children as tree structure for debugging
    def tree(self, indent: int = 0):
        print(" " * indent + self.name)
        for child in self.children:
            child.tree(indent + 2)