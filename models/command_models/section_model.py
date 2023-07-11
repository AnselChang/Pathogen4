from typing import TYPE_CHECKING
from adapter.path_adapter import NullPathAdapter
from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from models.command_models.abstract_model import AbstractModel, SerializedRecursiveState
from entities.root_container.panel_container.command_block_section.section_entity import SectionEntity
from models.command_models.command_model import CommandModel

"""
Model for a command section, which contains commands
"""

class SerializedSectionState(SerializedRecursiveState):

    def __init__(self, sectionName: str):
        super().__init__()
        self.sectionName = sectionName

    def _deserialize(self) -> 'CommandModel':
        model = SectionModel()
        model._sectionName = self.sectionName
        return model

class SectionModel(AbstractModel):

    def _serialize(self) -> SerializedSectionState:
        return SerializedSectionState(self._sectionName)
    
    def __init__(self):

        super().__init__()

        self._sectionName = "New Section"

    def getName(self):
        return self._sectionName
    
    def setName(self, name: str):
        print("set name", name)
        self._sectionName = name

    def _generateUIForMyself(self) -> ModelBasedEntity | Entity:
        return SectionEntity(None, self)
    
    def _canHaveChildren(self) -> bool:
        return True
    
    def _createChild(self) -> 'CommandModel':
        return CommandModel(NullPathAdapter())
    