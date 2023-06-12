from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
from models.command_models.model_based_entity import ModelBasedEntity


class FullContainer(Container, ModelBasedEntity):
    
    def __init__(self, parent: Entity):
        super().__init__(parent = parent)

        self.vgc = VariableGroupContainer(self, isHorizontal = False)

    def getChildVGC(self) -> VariableGroupContainer:
        return self.vgc

    def defineWidth(self) -> float:
        return self._pwidth(1)
    
    def defineHeight(self) -> float:
        return self._pheight(1)
    
    def defineLeftX(self) -> float:
        return self._px(0)
    
    def defineTopY(self) -> float:
        return self._py(0)