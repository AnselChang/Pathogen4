from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.group.radio_group_entity import RadioGroupEntity

from entity_base.entity import Entity
from entity_ui.group.linear_entity import LinearEntity
from common.reference_frame import PointRef
from entity_base.listeners.click_listener import ClickLambda
from typing import TypeVar, Generic

"""
A single option object for a RadioGroup
"""
T = TypeVar('T')
class RadioEntity(Generic[T], LinearEntity['RadioGroupEntity' | T]):

    def __init__(self, group: RadioGroupEntity | T, id: str):
        super().__init__(group, id)

    def onClick(self):
        self.group.onOptionClick(self)

    def isOn(self):
        return self.group.isOptionOn(self)