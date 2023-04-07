from entity_base.entity import Entity
from entity_base.static_entity import StaticEntity
from entity_base.entity import initEntityClass, setRootContainer

from root_container.field_container.node.path_node_entity import PathNodeEntity
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity

from root_container.panel_container.tab.tab_handler import TabHandler

from entity_handler.entity_manager import EntityManager
from entity_handler.interactor import Interactor

from root_container.path import Path

from command_creation.command_definition_database import CommandDefinitionDatabase
from command_creation.command_block_entity_factory import CommandBlockEntityFactory

from root_container.panel_container.command_expansion.command_expansion_handler import CommandExpansionHandler

from root_container.panel_container.panel_container import PanelContainer
from root_container.field_container.field_container import FieldContainer
from root_container.panel_container.command_scrolling.command_scrollbar import CommandScrollbar

from entity_ui.tooltip import initTooltipFont

from common.font_manager import FontManager, FontID
from common.image_manager import ImageManager, ImageID
from common.reference_frame import PointRef, Ref, initReferenceframe, VectorRef
from common.field_transform import FieldTransform
from common.dimensions import Dimensions
from common.draw_order import DrawOrder
from utility.pygame_functions import getGradientSurface
from utility.math_functions import isInsideBox2
import pygame, random
import sys

import cProfile


pygame.init()
pygame.key.set_repeat(400, 70)

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]

def main():

    # Initialize field
    dimensions = Dimensions()
    fontManager = FontManager(dimensions)
    screen = dimensions.resizeScreen(dimensions.DEFAULT_SCREEN_WIDTH, dimensions.DEFAULT_SCREEN_HEIGHT)

    images = ImageManager()
    imageSize = images.get(ImageID.FIELD).get_width()
    dimensions.setFieldSizePixels(imageSize)


    fieldTransform: FieldTransform = FieldTransform(images, dimensions)
    initReferenceframe(dimensions, fieldTransform)
    mouse: PointRef = PointRef()
    
    initTooltipFont(fontManager.getDynamicFont(FontID.FONT_NORMAL, 15))
    
    # Initialize entities
    interactor = Interactor(dimensions, fieldTransform)
    entities = EntityManager()
    initEntityClass(entities, interactor, images, fontManager, dimensions)
    rootContainer = entities.initRootContainer()
    setRootContainer(rootContainer)

    # Add permanent static entities
    panelColor = (100,100,100)
    panelContainer = PanelContainer(panelColor)
    fieldContainer = FieldContainer(fieldTransform)

    StaticEntity(lambda: interactor.drawSelectBox(screen), drawOrder = DrawOrder.MOUSE_SELECT_BOX)

    # create tabs
    tabHandler = TabHandler(panelContainer)

    # initialize commands
    database = CommandDefinitionDatabase()
    commandExpansion = CommandExpansionHandler(panelContainer)
    commandEntityFactory = CommandBlockEntityFactory(database, commandExpansion)

    # Create path
    path = Path(fieldContainer, panelContainer, database, commandEntityFactory, commandExpansion, PointRef(Ref.FIELD, (24,24)))

    # Add the gradient at the bottom of the commands
    c1 = (*panelColor, 255)
    c2 = (*panelColor, 0)
    height = 30
    offset = 35
    StaticEntity(
        lambda: screen.blit(getGradientSurface(dimensions.PANEL_WIDTH, height, c1, c2, invert=True), (dimensions.FIELD_WIDTH, dimensions.SCREEN_HEIGHT - height - offset)),
        drawOrder = DrawOrder.GRADIENT_PANEL,
    )
    StaticEntity(lambda: pygame.draw.rect(screen, panelColor, [dimensions.FIELD_WIDTH, dimensions.SCREEN_HEIGHT - offset, dimensions.PANEL_WIDTH, offset]), drawOrder = DrawOrder.GRADIENT_PANEL)
    
    # add grey rect at top to prevent commands from bleeding into panel
    height = 30
    height2 = 20
    StaticEntity(
        lambda: pygame.draw.rect(screen, panelColor, [dimensions.FIELD_WIDTH, 0, dimensions.PANEL_WIDTH, height]),
        drawOrder = DrawOrder.GRADIENT_PANEL
    )
    StaticEntity(
        lambda: screen.blit(getGradientSurface(dimensions.PANEL_WIDTH, height2, c1, c2), (dimensions.FIELD_WIDTH, height)),
        drawOrder = DrawOrder.GRADIENT_PANEL,
    )


    # initialize pygame artifacts
    pygame.display.set_caption("Pathogen 4.0 (Ansel Chang)")
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        mouse.screenRef = pygame.mouse.get_pos()
        interactor.setHoveredEntity(entities.getEntityAtPosition(mouse.screenRef), mouse)

        # handle events and call callbacks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = dimensions.resizeScreen(*event.size)
                fieldTransform.resizeScreen()
            elif event.type == pygame.MOUSEWHEEL and mouse.screenRef[0] < dimensions.FIELD_WIDTH:
                fieldTransform.changeZoom(mouse, event.y * 0.1)
            elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                ctrlKey = pygame.key.get_pressed()[pygame.K_LCTRL]
                shiftKey = pygame.key.get_pressed()[pygame.K_LSHIFT]
                right = (event.button == 1 and ctrlKey) or event.button == 3
                interactor.onMouseDown(entities, mouse, right, shiftKey)

            elif event.type == pygame.MOUSEBUTTONUP:
                interactor.onMouseUp(entities, mouse, path)

            elif event.type == pygame.MOUSEMOTION:
                interactor.onMouseMove(entities, mouse)

            elif event.type == pygame.KEYDOWN:
                entities.onKeyDown(event.key)

            elif event.type == pygame.KEYUP:
                entities.onKeyUp(event.key)

        # Perform calculations
        entities.tick()

        # Draw everything
        entities.drawEntities(interactor, screen, mouse.screenRef, dimensions)

        # Update display and maintain frame rate
        pygame.display.flip()
        clock.tick(60) # fps

if __name__ == "__main__":
    #cProfile.run('main()', sort='cumtime')
    main()
