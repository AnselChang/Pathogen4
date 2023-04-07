from entity_base.entity import Entity
from entity_ui.group.radio_entity import RadioEntity
from entity_ui.group.linear_group_entity import LinearGroupEntity
from entity_handler.entity_manager import EntityManager
from typing import TypeVar, Generic

"""a group of radio_entities, where only one is selected at a time
If allowNoSelect is True, then no option being selected is allowed
"""
T = TypeVar('T')
class RadioGroupEntity(Generic[T], LinearGroupEntity[RadioEntity | T]):

    def __init__(self, parent: Entity, isHorizontal: bool, allowNoSelect: bool = False):
        
        super().__init__(parent, isHorizontal)

        self.active: RadioEntity | T = None
        self.allowNoSelect = allowNoSelect


    def add(self, entity: RadioEntity):

        assert(isinstance(entity, RadioEntity))

        result = super().add(entity)
        if not self.allowNoSelect and self.active is None:
            self.active = entity

        return result


    def onOptionClick(self, option: RadioEntity):
        
        if option not in self.groupEntities:
            raise Exception("given RadioEntity object is not a part of this RadioGroup object")
        
        # toggle off, is no selection allowed
        if self.allowNoSelect and option is self.active:
            self.active = None
        else:
            self.active = option

    # get the active option
    def getActiveOption(self) -> RadioEntity | T:
        return self.active
    
    def isOptionOn(self, optionAsEntityOrID: str | RadioEntity):

        if not isinstance(optionAsEntityOrID, RadioEntity):
            optionAsEntityOrID = self.getFromID(optionAsEntityOrID)

        return self.active is optionAsEntityOrID
    
    def setOption(self, id: str | RadioEntity | None):
        if id is None:
            self.active = None
        elif isinstance(id, RadioEntity):
            self.active = id
        else:
            self.active = self.getFromID(id)