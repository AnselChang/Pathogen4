from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.group.radio_group_container import RadioGroupContainer

from entity_base.entity import Entity
from entity_ui.group.linear_container import LinearContainer
from common.reference_frame import PointRef
from entity_base.listeners.click_listener import ClickLambda
from typing import TypeVar, Generic

"""
A single option object for a RadioGroup
"""
T = TypeVar('T')
class RadioContainer(Generic[T], LinearContainer['RadioGroupEntity' | T]):

    def __init__(self, group: RadioGroupContainer | T, id: str):
        super().__init__(group, id)

    def onClick(self, mouse: tuple):
        self.group.onOptionClick(self)

    def isOn(self):
        return self.group.isOptionOn(self)