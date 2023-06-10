from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.command_models.abstract_model import AbstractModel

from entity_base.entity import Entity
from entity_ui.group.variable_group.variable_container import VariableContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer

"""
An interface for an UI element (path section / command / etc) that
can be built from a command model (see models/command_models/command_model.py
"""

class ModelBasedEntity:

    def __init__(self, model):
        self.model = model

    def clearChildUI(self) -> None:
        self.getChildVGC().containers.clear()

    # add a child UI element to this UI element
    def addChildUI(self, childUI: Entity) -> None:
        vc = VariableContainer(self.getChildVGC(), False)
        vc.setChild(childUI)
        childUI.changeParent(vc)
        self.getChildVGC().containers.addToEnd(vc)
    
    def getChildVGC(self) -> VariableGroupContainer:
        raise NotImplementedError