from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from models.command_models.abstract_model import AbstractModel
from models.command_models.section_model import SectionModel
from entities.root_container.panel_container.command_block.full_container import FullContainer
from serialization.serializable import Serializable, SerializedState
import copy

"""
Model of entire path command, through a list of path sections
"""

class SerializedCommandsState(SerializedState):
    
    def __init__(self, fullModel: 'FullCommandsModel'):
        self.fullModel = fullModel

class FullCommandsModel(AbstractModel[None, SectionModel], Serializable[SerializedCommandsState]):

    """
    Serialization works a bit differently with this model, since it's recursive.
    The easiest way I could think of was to deep copy the entire model,
    then go through the model and set all ui references to None.
    """
    def serialize(self) -> SerializedCommandsState:
        fullModelCopy = copy.deepcopy(self)
        fullModelCopy.resetUIToNone()
        fullModelCopy.fullModelParentUI = None
        return SerializedCommandsState(fullModelCopy)

    @staticmethod
    def deserialize(state: SerializedCommandsState) -> 'FullCommandsModel':
        return state.fullModel
    
    def __init__(self):
        super().__init__()

    def initParentUI(self, parentUI: Entity) -> None:

        self.fullModelParentUI = parentUI

        self.rebuild()

        # create the first section
        self.addSectionToEnd()


    def recomputeUI(self) -> None:
        self.ui.recomputeEntity()

    def getName(self):
        return "FullModel"

    def getParentUI(self) -> Entity:
        return self.fullModelParentUI
    
    def getParentVGC(self) -> Entity:
        return self.getParentUI()
    
    def _generateUIForMyself(self) -> ModelBasedEntity | Entity:
        return FullContainer(self.getParentUI(), self)

    def _canHaveChildren(self) -> bool:
        return True

    def _createChild(self) -> SectionModel:
        return SectionModel()
    
    def addSectionToEnd(self):
        self.insertChildAtEnd(self._createChild())