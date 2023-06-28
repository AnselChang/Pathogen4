"""
Resolves the position of a top bar entity given a percentage px,
which is a percent of the horizontal span of the top bar
"""

from typing import Callable
from common.image_manager import ImageID
from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
from entity_ui.group.variable_group.fixed_container import FixedContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer

class TopBarButtonState:

    def __init__(self, imageID: ImageID, onClick: Callable, tooltip: str):
        self.state = ImageState(0, imageID, tooltip)
        self.onClick = onClick


class TopBarButtonContainer(Container):

    def __init__(self, parent: Entity,
                 percent: float, # percent of top bar horizontal span
                 buttons: TopBarButtonState | list[TopBarButtonState], # info for one or more buttons,
                 padding: float = 0 # padding between buttons (relative pixels)
                 ):
        super().__init__(parent)
        self.percent = percent

        self.buttons = VariableGroupContainer(self, isHorizontal = True,
            innerMargin = padding,
            outerMargin = 0
        )

        # make sure buttons is a list of at least one element
        if not isinstance(buttons, list):
            buttons = [buttons]

        for button in buttons:
            fc = FixedContainer(self.buttons, True, lambda: self.defineHeight())
            image = ImageEntity(fc, button.state, onClick = button.onClick)


    def defineCenterX(self) -> float:
        return self._px(self.percent)
    
    def defineCenterY(self) -> float:
        return self._py(0.5)
    
    def defineWidth(self) -> float:
        return 0
    
    # each button is this proportion of the top bar height
    def defineHeight(self) -> float:
        return self._pheight(0.3)