from typing import TYPE_CHECKING
from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from models.command_models.abstract_model import AbstractModel
from root_container.panel_container.command_block_section.section_entity import SectionEntity
if TYPE_CHECKING:
    from models.command_models.full_model import FullModel
    from models.command_models.command_model import CommandModel

"""
Model for a command section, which contains commands
"""

class SectionModel(AbstractModel):
    
    def __init__(self, parent: 'FullModel'):

        super().__init__(parent)

    def _generateUIForMyself(self) -> ModelBasedEntity | Entity:
        return SectionEntity(self.getParentUI())
    
    def _canHaveChildren(self) -> bool:
        return True
    
    def _createChild(self) -> 'CommandModel':
        return self.createCustomCommandModel()
    