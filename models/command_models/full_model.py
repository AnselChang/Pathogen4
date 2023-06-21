from entity_base.entity import Entity
from models.command_models.model_based_entity import ModelBasedEntity
from models.command_models.abstract_model import AbstractModel
from models.command_models.section_model import SectionModel
from root_container.panel_container.command_block.full_container import FullContainer

"""
Model of entire path command, through a list of path sections
"""

class FullModel(AbstractModel[None, SectionModel]):
    
    def __init__(self, parentUI: Entity = None):
        super().__init__()

        self.fullModelParentUI = parentUI

        self.rebuild()

        # create the first section
        self.addSectionToEnd()

        print("after first section:")
        self.ui.tree()

    def recomputeUI(self) -> None:
        self.ui.recomputeEntity()

    def getName(self):
        return "FullModel"

    def getParentUI(self) -> Entity:
        return self.fullModelParentUI
    
    def getParentVGC(self) -> Entity:
        return self.getParentUI()
    
    def _generateUIForMyself(self) -> ModelBasedEntity | Entity:
        return FullContainer(self.getParentUI())

    def _canHaveChildren(self) -> bool:
        return True

    def _createChild(self) -> SectionModel:
        return SectionModel()
    
    def addSectionToEnd(self):
        self.insertChildAtEnd(self._createChild())