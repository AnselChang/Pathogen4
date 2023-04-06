from EntityHandler.entity_manager import EntityManager
from UIEntities.image_radio_entity import ImageRadioEntity
from UIEntities.radio_group_entity import RadioGroupEntity
from image_manager import ImageManager, ImageID
from Observers.observer import Observable
from dimensions import Dimensions
from pygame_functions import brightenSurface
from enum import Enum, auto

"""
Manage expanding and collapsing commands
Handles the forceExpand and forceCollapse buttons at the bottom of the panel
"""

class ButtonID(Enum):
    COLLAPSE = auto()
    EXPAND = auto()

class CommandExpansion(Observable):

    def partition(self, dimensions: Dimensions, i, n):
        return dimensions.FIELD_WIDTH + (i+1) * dimensions.PANEL_WIDTH / (n+1)

    def __init__(self, images: ImageManager, dimensions: Dimensions):

        self.buttons: RadioGroupEntity = RadioGroupEntity(True)
        y = lambda: dimensions.SCREEN_HEIGHT - self.buttons.options[0].height * 0.8

        info = [
            {
                "px" : 0.333,
                "imageOn" : ImageID.MIN_ON,
                "imageOff" : ImageID.MIN_OFF,
                "tooltip" : "Collapse all commands"
            },
            {
                "px" : 0.667,
                "imageOn" : ImageID.MAX_ON,
                "imageOff" : ImageID.MAX_OFF,
                "tooltip" : "Expand all commands"
            }
        ]

        py = 0.9
        for i, dict in enumerate(info):
            minOn = images.get(dict["imageOn"])
            minOff = images.get(dict["imageOff"])
            x = lambda i=i: self.partition(dimensions, i, self.buttons.N()) 
            button = ImageRadioEntity(dict["px"], py, minOn, minOff, x, y, onUpdate = lambda isOn: self.notify(), tooltip = dict["tooltip"]) 
            self.buttons.add(button)

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

    