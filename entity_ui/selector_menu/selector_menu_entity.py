from entity_base.entity import Entity
from entity_base.image.image_entity import ImageEntity
from entity_ui.group.dynamic_group_container import DynamicGroupContainer

from common.draw_order import DrawOrder
from common.image_manager import ImageID
from entity_ui.group.linear_container import LinearContainer
from entity_ui.selector_menu.selector_menu_factory import MenuButtonDefinition

"""
The background of the selector menu. Background is drawn
Contains a DynamicGroupContainer, which contains menu buttons
This is an Entity, not a Container, because if clicked, it should not close the menu
This is because the lifetime of the SelectorMenu is solely when
the parent entity (the entity the menu is for) or its children are selected
The size of this entity is dynamic - it is set to the DynamicGroupContainer size 
"""

class SelectorMenuEntity(Entity):

    def __init__(self, selectedEntity: Entity, menuDefinitions: list[MenuButtonDefinition]):

        self.BUTTON_SIZE = 20 # LinearContainers should be BUTTON_SIZE x BUTTON_SIZE
        self.BUTTON_IMAGE_SCALE = 0.9 # to add additional padding between button images and menu background

        super().__init__(parent = selectedEntity,
                         drawOrder = DrawOrder.SELECTOR_MENU_BACKGROUND)
        
        self.group = DynamicGroupContainer(self, True, self.BUTTON_SIZE)


        for definition in menuDefinitions:
            buttonContainer = LinearContainer(self.group, definition.tooltipString)
            ImageEntity(parent = buttonContainer,
                imageID = definition.imageID,
                imageIDHovered = definition.imageHoveredID,
                tooltip = definition.tooltipString,
                onClick = lambda mouse: definition.action.onClick(selectedEntity, mouse),
                drawOrder = DrawOrder.SELECTOR_MENU_BUTTON,
                pwidth = self.BUTTON_IMAGE_SCALE,
                pheight = self.BUTTON_IMAGE_SCALE
            )
    