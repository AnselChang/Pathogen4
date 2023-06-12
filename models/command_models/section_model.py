from typing import TYPE_CHECKING
from adapter.path_adapter import NullPathAdapter
from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from models.command_models.abstract_model import AbstractModel
from root_container.panel_container.command_block_section.section_entity import SectionEntity
from models.command_models.command_model import CommandModel

"""
Model for a command section, which contains commands
"""

class SectionModel(AbstractModel):
    
    def __init__(self):

        super().__init__("SectionModel")

    def _generateUIForMyself(self) -> ModelBasedEntity | Entity:
        return SectionEntity(self.getParentUI())
    
    def _canHaveChildren(self) -> bool:
        return True
    
    def _createChild(self) -> 'CommandModel':
        return CommandModel(NullPathAdapter())
    