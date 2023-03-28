from UIEntities.radio_entity import RadioEntity

# a group of radio_entities, where only one is selected at a time
class RadioGroup:

    def __init__(self, entityManager):

        self.entityManager = entityManager

        self.options: list[RadioEntity] = []
        self.activeOption: int = 0

    def add(self, option: RadioEntity):
        self.options.append(option)
        option.setRadioGroup(self)
        self.entityManager.addEntity(option)

    def onClick(self, option: RadioEntity):
        
        if option not in self.options:
            raise Exception("given RadioEntity object is not a part of this RadioGroup object")
        
        self.activeOption = self.options.index(option)

    # get the active option
    def getEntity(self) -> RadioEntity:
        return self.options[self.activeOption]
    
    def getID(self) -> str:
        return self.getEntity().id
