from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from models.command_models.abstract_model import AbstractModel
from models.command_models.section_model import SectionModel

"""
Model of entire path command, through a list of path sections
"""

class FullModel(AbstractModel[None, SectionModel]):
    
    def __init__(self):
        super().__init__(None)

    def _canHaveChildren(self) -> bool:
        return True

    def _createChild(self) -> SectionModel:
        return SectionModel(self)
    
    def addSectionToEnd(self):
        self.insertChildAtEnd(self._createChild())