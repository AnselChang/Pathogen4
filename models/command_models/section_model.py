from typing import TYPE_CHECKING
from entity_base.entity import Entity
from models.command_models.buildable_from_command_model import BuildableFromCommandModel
from models.command_models.abstract_model import AbstractModel
from root_container.panel_container.command_block_section.section_entity import SectionEntity
if TYPE_CHECKING:
    from models.command_models.full_model import FullModel
    from models.command_models.command_model import CommandModel

"""
Model for a command section, which contains commands
"""

class SectionModel(AbstractModel[FullModel, CommandModel]):
    
    def __init__(self, parent: FullModel):

        super().__init__(parent)

    def generateUIForMyself(self) -> BuildableFromCommandModel | Entity:
        return SectionEntity(None)
    
    def canHaveChildren(self) -> bool:
        return True
    
    def createChild(self) -> CommandModel:
        return self.createCustomCommandModel()
    