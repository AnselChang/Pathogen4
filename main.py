from BaseEntity.static_entity import StaticEntity

from NodeEntities.path_node_entity import PathNodeEntity
from SegmentEntities.path_segment_entity import PathSegmentEntity

from UIEntities.radio_group import RadioGroup
from UIEntities.tab_entity import TabEntity

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from PathData.path import Path

from CommandCreation.command_definition_database import CommandDefinitionDatabase
from CommandCreation.command_block_entity_factory import CommandBlockEntityFactory

from Commands.command_expansion import CommandExpansion

from TextEditor.static_text_editor_entity import StaticTextEditorEntity

from Tooltips import tooltip
from font_manager import FontManager, FontID
from image_manager import ImageManager, ImageID
from reference_frame import PointRef, Ref, initReferenceframe, VectorRef
from field_transform import FieldTransform
from dimensions import Dimensions
from draw_order import DrawOrder
from pygame_functions import getGradientSurface
from math_functions import isInsideBox2
import pygame, random
import sys

import cProfile


pygame.init()
pygame.key.set_repeat(400, 70)

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]

def initTabs(dimensions, entities, fontManager: FontManager) -> RadioGroup:
    tabs = RadioGroup(entities)
    tabNames = ["A", "B", "C"]

    N = len(tabNames)
    for i, text in enumerate(tabNames):
        tabs.add(TabEntity(dimensions, fontManager.getDynamicFont(FontID.FONT_NORMAL, 15), text, i, N))
    return tabs

def drawPanelBackground(screen, dimensions, panelColor):
    # draw panel
        x, y = dimensions.FIELD_WIDTH, 0
        width, height = dimensions.PANEL_WIDTH, dimensions.SCREEN_HEIGHT
        pygame.draw.rect(screen, panelColor, (x, y, width, height))

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
    
    tooltip.setTooltipFont(fontManager.getDynamicFont(FontID.FONT_NORMAL, 15))
    
    # Initialize entities
    interactor = Interactor(dimensions, fieldTransform)
    entities = EntityManager()

    # initialize commands
    database = CommandDefinitionDatabase(entities, interactor, images, dimensions)
    commandExpansion = CommandExpansion(entities, images, dimensions)
    commandEntityFactory = CommandBlockEntityFactory(database, entities, interactor, commandExpansion, images, fontManager, dimensions)

    # Create path
    path = Path(database, entities, interactor, commandEntityFactory, commandExpansion, dimensions, PointRef(Ref.FIELD, (24,24)))


    # Create tabs
    tabs = initTabs(dimensions, entities, fontManager)


    # Add permanent static entities
    panelColor = (100,100,100)
    entities.addEntity(StaticEntity(lambda: screen.fill((255,255,255)), drawOrder = DrawOrder.BACKGROUND))
    entities.addEntity(StaticEntity(lambda: fieldTransform.draw(screen), drawOrder = DrawOrder.FIELD_BACKGROUND))
    entities.addEntity(StaticEntity(lambda: drawPanelBackground(screen, dimensions, panelColor), drawOrder = DrawOrder.PANEL_BACKGROUND))
    entities.addEntity(StaticEntity(lambda: interactor.drawSelectBox(screen), drawOrder = DrawOrder.MOUSE_SELECT_BOX))

    # Add the gradient at the bottom of the commands
    c1 = (*panelColor, 255)
    c2 = (*panelColor, 0)
    height = 30
    offset = 35
    entities.addEntity(StaticEntity(
        lambda: screen.blit(getGradientSurface(dimensions.PANEL_WIDTH, height, c1, c2, invert=True), (dimensions.FIELD_WIDTH, dimensions.SCREEN_HEIGHT - height - offset)),
        Ftouching = lambda position: isInsideBox2(*position.screenRef, dimensions.FIELD_WIDTH, dimensions.SCREEN_HEIGHT - offset - height/2, dimensions.PANEL_WIDTH, offset + height/2),
        drawOrder = DrawOrder.GRADIENT_PANEL,
    ))
    entities.addEntity(StaticEntity(lambda: pygame.draw.rect(screen, panelColor, [dimensions.FIELD_WIDTH, dimensions.SCREEN_HEIGHT - offset, dimensions.PANEL_WIDTH, offset]), drawOrder = DrawOrder.GRADIENT_PANEL))
    
    # add grey rect at top to prevent commands from bleeding into panel
    height = 30
    height2 = 20
    entities.addEntity(StaticEntity(
        lambda: pygame.draw.rect(screen, panelColor, [dimensions.FIELD_WIDTH, 0, dimensions.PANEL_WIDTH, height]),
        Ftouching = lambda position: isInsideBox2(*position.screenRef, dimensions.FIELD_WIDTH, 0, dimensions.PANEL_WIDTH, height + height2/2),
        drawOrder = DrawOrder.GRADIENT_PANEL
    ))
    entities.addEntity(StaticEntity(
        lambda: screen.blit(getGradientSurface(dimensions.PANEL_WIDTH, height2, c1, c2), (dimensions.FIELD_WIDTH, height)),
        drawOrder = DrawOrder.GRADIENT_PANEL,
    ))

    # test text box
    #textbox = StaticTextEditorEntity(300, 300, 100, 100, (239, 226, 174), (174, 198, 239))
    #entities.addEntity(textbox)

    # initialize pygame artifacts
    pygame.display.set_caption("Pathogen 4.0 (Ansel Chang)")
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        mouse.screenRef = pygame.mouse.get_pos()
        interactor.setHoveredEntity(entities.getEntityAtPosition(mouse), mouse)

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
