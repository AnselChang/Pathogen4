
"""
An interface for an UI element (path section / command / etc) that
can be built from a command model (see models/command_models/command_model.py
"""

from entity_base.entity import Entity
from entity_ui.group.variable_group.variable_container import VariableContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer


class BuildableFromCommandModel:

    def clearChildUI(self) -> None:
        self.getVGC().containers.clear()

    # add a child UI element to this UI element
    def addChildUI(self, childUI: Entity) -> None:
        vc = VariableContainer(self.getVGC(), False)
        vc.setChild(childUI)
        childUI.changeParent(vc)
        self.getVGC().containers.addToEnd(vc)
    
    def getVGC(self) -> VariableGroupContainer:
        raise NotImplementedError