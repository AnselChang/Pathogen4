from entity_base.image.toggle_image_entity import ToggleImageEntity
from entity_ui.group.radio_container import RadioContainer
from root_container.panel_container.command_expansion.expansion_group_entity import ExpansionGroupEntity
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

class CommandExpansionHandler(Observable):

    def partition(self, dimensions: Dimensions, i, n):
        return dimensions.FIELD_WIDTH + (i+1) * dimensions.PANEL_WIDTH / (n+1)

    def __init__(self, panelEntity):

        info = [
            {
                "id" : ButtonID.COLLAPSE,
                "imageOn" : ImageID.MIN_ON,
                "imageOff" : ImageID.MIN_OFF,
                "tooltip" : "Collapse all commands"
            },
            {
                "id" : ButtonID.EXPAND,
                "imageOn" : ImageID.MAX_ON,
                "imageOff" : ImageID.MAX_OFF,
                "tooltip" : "Expand all commands"
            }
        ]

        self.buttons = ExpansionGroupEntity(panelEntity)
        for dict in info:
            id = dict["id"]
            radio = RadioContainer(self.buttons, id)
            ToggleImageEntity(radio, dict["imageOn"], dict["imageOff"],
                        drawOrder = DrawOrder.UI_BUTTON,
                        tooltip = dict["tooltip"],
                        onClick = radio.onClick,
                        isOn = lambda id=id: radio.group.isOptionOn(id)
            )
            

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

    