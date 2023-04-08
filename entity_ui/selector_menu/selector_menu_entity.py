from entity_base.entity import Entity
from entity_base.image.image_entity import ImageEntity
from entity_ui.group.dynamic_group_container import DynamicGroupContainer

from common.draw_order import DrawOrder
from common.image_manager import ImageID
from entity_ui.group.linear_container import LinearContainer
from entity_ui.selector_menu.selector_menu_factory import MenuButtonDefinition
from root_container.field_container.field_container import FieldContainer
import pygame

"""
The background of the selector menu. Background is drawn
Contains a DynamicGroupContainer, which contains menu buttons
This is an Entity, not a Container, because if clicked, it should not close the menu
This is because the lifetime of the SelectorMenu is solely when
the parent entity (the entity the menu is for) or its children are selected
The size of this entity is dynamic - it is set to the DynamicGroupContainer size 

Composition structure:
    - SelectorMenuEntity
        - DynamicGroupContainer
            - LinearContainer
                - ImageEntity
            - LinearContainer
                - ImageEntity
            - etc.
"""

class SelectorMenuEntity(Entity):

    def __init__(self, fieldContainer: FieldContainer, selectedEntity: Entity, menuDefinitions: list[MenuButtonDefinition]):
        print("Spawn")
        self.BUTTON_SIZE = 20 # LinearContainers should be BUTTON_SIZE x BUTTON_SIZE. Relative pixel units
        self.BUTTON_IMAGE_SCALE = 0.9 # to add additional padding between button images and menu background

        self.MENU_COLOR = [255, 204, 153]
        self.BORDER_RADIUS = 5

        super().__init__(parent = selectedEntity,
                         drawOrder = DrawOrder.SELECTOR_MENU_BACKGROUND)
        
        self.pxOfField, self.pyOfField = self.findStartingPosition(fieldContainer, selectedEntity)
        self.fieldContainer = fieldContainer

        self.group: DynamicGroupContainer = None
        self.recomputePosition()
        
        self.group = DynamicGroupContainer(self, True, self.BUTTON_SIZE)

        # Create a menu button container and image for each menu.
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

    # Remove itself and all children from the screen
    def despawn(self):
        self.entities.removeEntity(self)
        print("despawn")

    """
    Based on the position of the entity on the field, we need to determine where
    to spawn the menu. The menu should be spawned in a way where it is closest
    to the center of the FieldContainer, but not overlapping the entity,
    and preferably in open space.
    It should be returned in units of percent relative to FieldContainer
    """
    def findStartingPosition(self, fieldContainer: FieldContainer, selectedEntity: Entity) -> tuple[float, float]:

        # For now, we go with the simplest implementation,
        # which is to spawn the menu at the center of the field
        return 0.5, 0.5
    
    # dynamically bounded to the size of the DynamicGroupContainer
    def defineWidth(self) -> float:
        if self.group is None:
            return 0
        return self.group.defineWidth()
    
    # Match button width and height
    def defineHeight(self) -> float:
        return self._aheight(self.BUTTON_SIZE)
    
    # From the position calculated in findStartingPosition(), convert
    # from percent relative to FieldContainer to absolute units
    def defineCenter(self) -> tuple:
        return self.fieldContainer._px(self.pxOfField), self.fieldContainer._py(self.pyOfField)
    
    # Draws the background of the menu
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):
        pygame.draw.rect(screen, self.MENU_COLOR, self.RECT, border_radius = self.BORDER_RADIUS)
