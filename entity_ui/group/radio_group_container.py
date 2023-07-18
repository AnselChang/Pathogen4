from common.draw_order import DrawOrder
from data_structures.observer import Observable
from entity_base.entity import Entity
from entity_ui.group.radio_container import RadioContainer
from entity_ui.group.linear_group_container import LinearGroupContainer
from entity_handler.entity_manager import EntityManager
from typing import TypeVar, Generic

"""a group of radio_entities, where only one is selected at a time
If allowNoSelect is True, then no option being selected is allowed
"""
T = TypeVar('T')
class RadioGroupContainer(Generic[T], LinearGroupContainer[RadioContainer | T], Observable):

    def __init__(self, parent: Entity, isHorizontal: bool, allowNoSelect: bool = False):
        
        super().__init__(parent, isHorizontal, drawOrder)

        self.active: RadioContainer | T = None
        self.allowNoSelect = allowNoSelect


    def add(self, entity: RadioContainer):

        assert(isinstance(entity, RadioContainer))

        result = super().add(entity)
        if not self.allowNoSelect and self.active is None:
            self.active = entity

        return result


    def onOptionClick(self, option: RadioContainer):
        
        if option not in self.groupEntities:
            raise Exception("given RadioEntity object is not a part of this RadioGroup object")
        
        # toggle off, is no selection allowed
        if self.allowNoSelect and option is self.active:
            self.active = None
        else:
            # option is already set
            if self.active is option:
                return

            self.active = option
        self.notify()

    # get the active option
    def getActiveOption(self) -> RadioContainer | T:
        return self.active
    
    def isOptionOn(self, optionAsEntityOrID: str | RadioContainer):

        if not isinstance(optionAsEntityOrID, RadioContainer):
            optionAsEntityOrID = self.getFromID(optionAsEntityOrID)

        return self.active is optionAsEntityOrID
    
    def setOption(self, id: str | RadioContainer | None):
        if id is None:
            self.active = None
        elif isinstance(id, RadioContainer):
            self.active = id
        else:
            self.active = self.getFromID(id)