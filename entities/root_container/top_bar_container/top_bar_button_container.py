"""
Resolves the position of a top bar entity given a percentage px,
which is a percent of the horizontal span of the top bar
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, TypeVar
from common.image_manager import ImageID
from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
from entity_ui.group.variable_group.fixed_container import FixedContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer

# Implement this to define button behavior
class ButtonClickAction(ABC):

    # override this to return current state ID of the button
    # For buttons with only a single state, do not need to overwrite
    def getStateID(self) -> Enum:
        return None
        
    # if not available, the button will be grayed out, and cannot be clicked
    def isActionAvailable(self) -> bool:
        return True

    # callback for when button is both available and clicked
    @abstractmethod
    def onClick(self):
        pass

    def _onClick(self, mouse):
        self.onClick()

# Simple use case for a Button action that just calls callback with single image state
class SimpleButtonClickAction(ButtonClickAction):
    def __init__(self, onClick: Callable):
        self._onClick = onClick

    def onClick(self):
        self._onClick()

# Used to construct a button
class ButtonDefinition:

    # onClick should take in TWO ARGUMENTS: the target entity and the mouse
    def __init__(self, imageStates: ImageState | list[ImageState], action: ButtonClickAction):
        
        if not isinstance(imageStates, list):
            imageStates = [imageStates]
        
        self.imageStates = imageStates
        self.action = action

# A simple template for constructing a button, when only needing single image, callback, and tooltip
class SimpleButtonDefinition(ButtonDefinition):

    def __init__(self, imageID: ImageID, onClick: Callable, tooltip: str):
        state = ImageState(0, imageID, tooltip)
        action = SimpleButtonClickAction(onClick)
        super().__init__(state, action)


class TopBarButtonContainer(Container):

    def __init__(self, parent: Entity,
                 percent: float, # percent of top bar horizontal span
                 buttonDefinitions: ButtonDefinition | list[ButtonDefinition], # info for one or more buttons,
                 padding: float = 0 # padding between buttons (relative pixels)
                 ):
        super().__init__(parent)
        self.percent = percent

        self.buttons = VariableGroupContainer(self, isHorizontal = True,
            innerMargin = padding,
            outerMargin = 0
        )

        # make sure buttons is a list of at least one element
        if not isinstance(buttonDefinitions, list):
            buttonDefinitions = [buttonDefinitions]

        # create the button from the definition
        for definition in buttonDefinitions:
            fc = FixedContainer(self.buttons, True, lambda: self.defineHeight())
            print(definition)
            image = ImageEntity(parent = fc,
                states = definition.imageStates,
                isOn = lambda definition=definition: definition.action.isActionAvailable(),
                onClick = lambda mouse, definition=definition: definition.action._onClick(mouse),
                getStateID = lambda definition=definition: definition.action.getStateID(),
            )


    def defineCenterX(self) -> float:
        return self._px(self.percent)
    
    def defineCenterY(self) -> float:
        return self._py(0.5)
    
    def defineWidth(self) -> float:
        return 0
    
    # each button is this proportion of the top bar height
    def defineHeight(self) -> float:
        return self._pheight(0.37)