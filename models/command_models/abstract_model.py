from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

from data_structures.linked_list import LinkedList, LinkedListNode
from typing import TypeVar, Generic

from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from entities.root_container.panel_container.command_block.command_inserter import CommandInserter
from serialization.serializable import Serializable, SerializedState


if TYPE_CHECKING:
    from entity_ui.group.variable_group.variable_container import VariableContainer


"""
A single-source-of-truth model storing the internal state of some
recursive element, like a command block or a section. It handles
the recursive generation of UI elements from the model for itself and its children,
and has the option to regenerate the UI for itself without needing
to regenerate the UI for its children through caching.
"""

class SerializedRecursiveState(SerializedState):

    def __init__(self):
        self.children: list[SerializedRecursiveState] = []

    def addChild(self, child: SerializedRecursiveState):
        self.children.append(child)

    def _deserialize(self) -> 'AbstractModel':
        raise NotImplementedError("Must implement this method")

T1 = TypeVar('T1') # parent type
T2 = TypeVar('T2') # children type
class AbstractModel(Serializable, Generic[T1, T2]):

    def _serialize(self) -> SerializedRecursiveState:
        raise NotImplementedError("Must implement this method")
    
    def serialize(self) -> SerializedRecursiveState:
        state = self._serialize()
        for child in self.children:
            state.addChild(child.serialize())
        return state

    @staticmethod
    def deserialize(state: SerializedRecursiveState) -> 'AbstractModel':
        model = state._deserialize()
        for childState in state.children:
            childModel = AbstractModel.deserialize(childState)
            model.children.append(childModel)
            childModel.parent = model
        return model

    def __init__(self):

        super().__init__()
        
        self.parent: 'AbstractModel' = None
        self.children: list[AbstractModel | T2] = []

        self.ui = None
        self.show = True

    def showUI(self):
        self.show = True
        if self.parent is not None:
            self.parent.rebuildChildren()

    def hideUI(self):
        self.show = False
        if self.parent is not None:
            self.parent.rebuildChildren()

    def resetUIToNone(self):
        self.ui = None
        for child in self.children:
            child.resetUIToNone()

    def getName(self):
        return "AbstractModel"
    
    def isTask(self) -> bool:
        return False

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
    
    def getPreviousSiblingModel(self) -> AbstractModel | T2:
        if self.parent is None:
            return None
        i = self.parent.getIndex(self)
        return None if i == 0 else self.parent.children[i-1]
    
    def getNextSiblingModel(self) -> AbstractModel | T2:
        if self.parent is None:
            return None
        i = self.parent.getIndex(self)
        return None if i == len(self.parent.children)-1 else self.parent.children[i+1]
    
    def getPreviousUI(self) -> ModelBasedEntity | Entity:
        if self.parent is None:
            return None
        
        vgc = self.parent.ui.getChildVGC()
        i = vgc._children.index(self.ui._parent)
        
        if i == 0:
            return None
        
        vc: VariableContainer = vgc._children[i-1]
        return vc.child
    
    def getNextUI(self) -> ModelBasedEntity | Entity:
        if self.parent is None:
            return None
        
        vgc = self.parent.ui.getChildVGC()
        i = vgc._children.index(self.ui._parent)
        
        if i == len(vgc._children)-1:
            return None
        
        vc: VariableContainer = vgc._children[i+1]
        return vc.child
    
    def getIndex(self, child: AbstractModel):
        return self.children.index(child)
    
    # insert a sibling model after this model
    def insertAfterThis(self, model: AbstractModel | T2) -> None:
        self.parent.insertChildAfter(model, self)

        model.rebuild()
        self.parent.rebuildChildren()

    # insert a sibling model before this model
    def insertBeforeThis(self, model: AbstractModel | T2) -> None:

        i = self.parent.getIndex(self)

        if i == 0:
            self.parent.insertChildAtBeginning(model)
        else:
            self.parent.insertChildAfter(model, self.parent.children[i-1])

        model.rebuild()
        self.parent.rebuildChildren()

    def insertChildAfter(self, model: AbstractModel | T2, after: AbstractModel | T2):
        model.parent = self

        i = self.getIndex(after)
        self.children.insert(i+1, model)

        model.rebuild()
        self.rebuildChildren()

    def insertChildAtBeginning(self, model: AbstractModel | T2):
        model.parent = self
        self.children.insert(0, model)

        model.rebuild()
        self.rebuildChildren()

    def insertChildAtEnd(self, model: AbstractModel | T2):
        model.parent = self
        self.children.append(model)

        model.rebuild()
        self.rebuildChildren()

    # relocate self to be after model.
    # Could be moved to anywhere in the tree (not necessarily sibling)
    def moveThisAfter(self, model: AbstractModel | T2) -> None:
        self.delete()
        model.insertAfterThis(self)

    # relocate self to be before model.
    # Could be moved to anywhere in the tree (not necessarily sibling)
    def moveThisBefore(self, model: AbstractModel | T2) -> None:
        self.delete()
        model.insertBeforeThis(self)

    def moveThisInsideParent(self, parent: AbstractModel | T1) -> None:
        self.delete()
        parent.insertChildAtEnd(self)

    def onInserterClicked(self, elementBeforeInserter: AbstractModel):

        sectionOrCommand = self._createChild()

        if elementBeforeInserter is None:
            self.insertChildAtBeginning(sectionOrCommand)
        else:
            self.insertChildAfter(sectionOrCommand, elementBeforeInserter)

        self.ui.recomputeEntity()


    def getRootModel(self) -> AbstractModel:
        if self.parent is None:
            return self
        return self.parent.getRootModel()
    
    def isRootModel(self) -> bool:
        return self.parent is None
    
    def isSectionModel(self) -> bool:
        # root model
        if self.isRootModel():
            return False
        
        return self.parent.parent is None
    
    def createInserterUI(self, elementBeforeInserter: AbstractModel) -> CommandInserter:
        return CommandInserter(None, self.getRootModel(), lambda: self.onInserterClicked(elementBeforeInserter), elementBeforeInserter is None)
    
    # return cached UI for this element
    def getExistingUI(self) -> ModelBasedEntity | Entity:
        assert(self.ui is not None)
        return self.ui
    
    # Delete this model
    def delete(self) -> None:
        if self.parent is not None:
            self.parent.children.remove(self)
            self.parent.rebuildChildren()
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
            return False
        
        # search for the child reference in the parent
        if self.parent.ui is None:
            raise Exception("Parent UI is None")
            
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
        return True
    
    # rebuild the UI for this element
    # Calls rebuildChildren() to link the UIs of the children to this
    def rebuild(self, recomputeChildren: bool = False) -> None:

        self.reassignSelfUI( self._generateUIForMyself() )
        
        if not isinstance(self.ui, ModelBasedEntity) and isinstance(self.ui, Entity):
            raise Exception("Model must generate ModelBasedEntity", self.ui)

        self.rebuildChildren(recomputeChildren)
        
    # Rebuild the children of this element. Do not recompute
    # the UI either for this element or the children,
    # just link existing reference to child UIs
    def rebuildChildren(self, recompute: bool = False):

        if not self._canHaveChildren():
            return
        
        self.ui.clearChildUI()
                
        # add first inserter UI
        self.ui.addChildUI(self.createInserterUI(None))

        for child in self.children:

            # command is hidden, don't show it
            if not child.show:
                continue

            if recompute:
                x = child.rebuild(recomputeChildren = True)

            assert(child.getExistingUI() is not None)

            # add the section/command UI
            self.ui.addChildUI(child.getExistingUI())

            # add the inserter UI
            self.ui.addChildUI(self.createInserterUI(child))

    # rebuild this element and all children fully
    def rebuildAll(self):
        self.rebuild(True)

    # print this element and all children as tree structure for debugging
    def tree(self, indent: int = 0):
        print(" " * indent + self.getName())
        for child in self.children:
            child.tree(indent + 2)