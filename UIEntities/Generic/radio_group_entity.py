from BaseEntity.entity import Entity
from UIEntities.Generic.radio_entity import RadioEntity
from UIEntities.Generic.linear_group_entity import LinearGroupEntity
from EntityHandler.entity_manager import EntityManager

"""a group of radio_entities, where only one is selected at a time
If allowNoSelect is True, then no option being selected is allowed
Child of Panel Entity
"""
class RadioGroupEntity(LinearGroupEntity):

    def __init__(self, allowNoSelect: bool = False):
        
        super().__init__()

        self.active: RadioEntity = None
        self.allowNoSelect = allowNoSelect


    def add(self, option: RadioEntity):
        self.options.append(option)
        option.setRadioGroup(self, self.N)
        self.entities.addEntity(option, self)

        if not self.allowNoSelect and self.active is None:
            self.active = option

        self.N += 1

    def onOptionClick(self, option: RadioEntity):
        
        if option not in self.options:
            raise Exception("given RadioEntity object is not a part of this RadioGroup object")
        
        # toggle off, is no selection allowed
        if self.allowNoSelect and option is self.active:
            self.active = None
        else:
            self.active = option

    # get the active option
    def getActiveEntity(self) -> RadioEntity:
        return self.active
    
    def getActiveID(self) -> str:
        return self.getActiveEntity().id
    
    def getOptionFromID(self, id) -> RadioEntity:
        for option in self.options:
            if option.id == id:
                return option
        raise Exception("No option with id found")

    def N(self) -> int:
        return len(self.options)
    
    def isOptionOn(self, id):
        if isinstance(id, RadioEntity):
            return id.isActive()
        else:
            return self.getOptionFromID(id).isActive()
    
    def setOption(self, id: int | RadioEntity | None):
        if id is None:
            self.active = None
        elif isinstance(id, RadioEntity):
            self.active = id
        else:
            self.active = self.getOptionFromID(id)