from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from UIEntities.Generic.linear_group_entity import LinearGroupEntity

from BaseEntity.entity import Entity
from UIEntities.Generic.linear_entity import LinearEntity
from reference_frame import PointRef
from BaseEntity.EntityListeners.click_listener import ClickLambda

"""
A single option object for a RadioGroup
"""
class RadioEntity(LinearEntity):

    def onClick(self):
        self.group.onOptionClick(self)

    def isOn(self):
        return self.group.isOptionOn(self)