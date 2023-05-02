from entity_base.container_entity import Container
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
from entity_ui.group.radio_container import RadioContainer
from entity_ui.group.radio_group_container import RadioGroupContainer
from common.image_manager import ImageID
from data_structures.observer import Observable
from common.dimensions import Dimensions
from common.draw_order import DrawOrder
from enum import Enum, auto

"""
Manage expanding and collapsing commands
Handles the forceExpand and forceCollapse buttons at the bottom of the panel
"""

class ButtonID(Enum):
    COLLAPSE = auto()
    EXPAND = auto()

class CommandExpansionContainer(Container, Observable):

    def partition(self, dimensions: Dimensions, i, n):
        return dimensions.FIELD_WIDTH + (i+1) * dimensions.PANEL_WIDTH / (n+1)

    def __init__(self, panelEntity):

        super().__init__(panelEntity, drawOrder = DrawOrder.UI_BUTTON)
        self.recomputePosition()

        info = [
            {
                "id" : ButtonID.COLLAPSE,
                "imageOn" : ImageID.MIN_ON,
                "imageOff" : ImageID.MIN_OFF,
                "tooltip" : "Collapse"
            },
            {
                "id" : ButtonID.EXPAND,
                "imageOn" : ImageID.MAX_ON,
                "imageOff" : ImageID.MAX_OFF,
                "tooltip" : "Expand"
            }
        ]

        self.buttons = RadioGroupContainer(self, isHorizontal = True, allowNoSelect = True)
        for dict in info:
            id = dict["id"]
            radio = RadioContainer(self.buttons, id)

            tooltip = dict["tooltip"]

            states = [
                ImageState(True, dict["imageOn"], f"{tooltip} all commands: enabled"),
                ImageState(False, dict["imageOff"], f"{tooltip} all commands: disabled")
            ]
            ImageEntity(parent = radio,
                        states = states,
                        drawOrder = DrawOrder.UI_BUTTON,
                        onClick = lambda mouse, radio=radio: self.onClick(radio, mouse),
                        getStateID = lambda id=id: radio.group.isOptionOn(id)
            )

    def onClick(self, radioButton: RadioContainer, mouse: tuple):
        radioButton.onClick(mouse)
        self.notify()
            

    def setForceCollapse(self, isCollapse: bool):

        if isCollapse:
            self.buttons.setOption(ButtonID.COLLAPSE)
        else:
            self.buttons.setOption(None)

        self.notify()

    def getForceCollapse(self) -> bool:
        return self.buttons.isOptionOn(ButtonID.COLLAPSE)

    def setForceExpand(self, isExpand: bool):

        if isExpand:
            self.buttons.setOption(ButtonID.EXPAND)
        else:
            self.buttons.setOption(None)

        self.notify()

    def getForceExpand(self) -> bool:
        return self.buttons.isOptionOn(ButtonID.EXPAND)

    def defineCenterX(self) -> float:
        return self._px(0.5)
    
    def defineBottomY(self) -> float:
        return self._py(0.95)

    def defineWidth(self) -> float:
        return self._pwidth(0.8)
    def defineHeight(self) -> float:
        return self._pheight(0.05)