from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.group.linear_group_entity import LinearGroupEntity

from entity_base.entity import Entity
from entity_ui.group.linear_entity import LinearEntity
from common.reference_frame import PointRef
from entity_base.listeners.click_listener import ClickLambda

"""
A single option object for a RadioGroup
"""
class RadioEntity(LinearEntity):

    def onClick(self):
        self.group.onOptionClick(self)

    def isOn(self):
        return self.group.isOptionOn(self)