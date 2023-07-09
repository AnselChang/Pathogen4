import math
from data_structures.observer import Observer
from entity_base.entity import Entity
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
from entity_base.listeners.drag_listener import DragLambda
from entity_ui.group.dynamic_group_container import DynamicGroupContainer

from common.draw_order import DrawOrder
from common.image_manager import ImageID
from entity_ui.group.linear_container import LinearContainer
from entity_ui.selector_menu.menu_line_entity import MenuLineEntity
from entity_ui.selector_menu.selector_menu_factory import MenuDefinition
from entities.root_container.field_container.field_container import FieldContainer
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

class SelectorMenuEntity(Entity, Observer):

    def __init__(self, fieldContainer: FieldContainer, selectedEntity: Entity, menuDefinition: MenuDefinition):
        self.BUTTON_SIZE = 20 # LinearContainers should be BUTTON_SIZE x BUTTON_SIZE. Relative pixel units
        self.BUTTON_IMAGE_SCALE = 0.7 # to add additional padding between button images and menu background

        self.MENU_COLOR = [255, 204, 153]
        self.BORDER_RADIUS = 5

        self.selectedEntity = selectedEntity
        selectedEntity.subscribe(self, onNotify = self.recomputeEntity)

        # Both this object and the individual menu images have this lambda.
        # So, when either the menu background or menu buttons are dragged,
        # move this
        dragLambda = DragLambda(self, selectedEntity,
                                           FonStartDrag = self.onStartDrag,
                                           FonDrag = self.onDrag,
                                           FonStopDrag = self.onStopDrag
                                           )

        super().__init__(parent = selectedEntity,
                         drag = dragLambda,
                         drawOrder = DrawOrder.SELECTOR_MENU_BACKGROUND,
                         drawOrderRecursive = False
                         )
        
        self.fieldContainer = fieldContainer

        self.relX = 10
        self.relY = 0

        self.group: DynamicGroupContainer = None
        self.recomputeEntity()
        
        self.group = DynamicGroupContainer(self, True, self.BUTTON_SIZE)

        # Create a menu button container and image for each menu
        for i, definition in enumerate(menuDefinition.definitions):

            if not definition.condition(selectedEntity):
                continue

            buttonContainer = LinearContainer(self.group, i)
            image = ImageEntity(parent = buttonContainer,
                states = definition.imageStates,
                isOn = lambda definition=definition: definition.action.isActionAvailable(selectedEntity),
                onClick = lambda mouse, definition=definition: definition.action.onClick(selectedEntity, mouse),
                getStateID = lambda definition=definition: definition.action.getStateID(selectedEntity),
                drawOrder = DrawOrder.SELECTOR_MENU_BUTTON,
                pwidth = self.BUTTON_IMAGE_SCALE,
                pheight = self.BUTTON_IMAGE_SCALE,
                drag = dragLambda
            )
        
        # need to recompute position again to determine correct width
        self.recomputeEntity()

        MenuLineEntity(self, selectedEntity)

    def getEntity(self) -> Entity:
        return self.selectedEntity

    # Remove itself and all children from the screen
    def despawn(self):
        if self in self.entities.entities:
            self.entities.removeEntity(self)

    # dynamically bounded to the size of the DynamicGroupContainer
    def defineWidth(self) -> float:
        if self.group is None:
            return 0
        return self.group.defineWidth()
    
    # Match button width and height
    def defineHeight(self) -> float:
        return self._aheight(self.BUTTON_SIZE)
    
    # Left edge of menu should be aligned with the entity
    def defineLeftX(self) -> float:
        return self._px(0.5) + self._awidth(self.relX)
    
    # Top edge of menu should be aligned of center of entity
    def defineTopY(self) -> float:
        return self._py(0.5) + self._aheight(self.relY)
    
    # Even if parent node is transparent, the menu should be opaque
    def getOpacity(self) -> float:
        return 1
    
    # Draws the background of the menu
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):

        pygame.draw.rect(screen, self.MENU_COLOR, self.RECT, border_radius = self.BORDER_RADIUS)

    def onStartDrag(self, mouse: tuple):
        self.startMouseX, self.startMouseY = mouse
        self.startRelX, self.startRelY = self.relX, self.relY

    def onDrag(self, mouse: tuple):
        deltaX, deltaY = mouse[0] - self.startMouseX, mouse[1] - self.startMouseY
        self.relX = self.startRelX + self._inverse_awidth(deltaX)
        self.relY = self.startRelY + self._inverse_aheight(deltaY)
        self.recomputeEntity()

    def onStopDrag(self):
        pass