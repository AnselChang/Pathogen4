from BaseEntity.static_entity import StaticEntity

from NodeEntities.path_node_entity import PathNodeEntity
from SegmentEntities.path_segment_entity import PathSegmentEntity

from UIEntities.radio_group import RadioGroup
from UIEntities.tab_entity import TabEntity

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from PathData.path import Path

from CommandCreation.command_builder import CommandBuilder

from image_manager import ImageManager
from reference_frame import PointRef, Ref, initReferenceframe, VectorRef
from field_transform import FieldTransform
from dimensions import Dimensions
from draw_order import DrawOrder
import pygame, random
import sys

pygame.init()

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]

def initTabs(dimensions, entities) -> RadioGroup:
    tabs = RadioGroup(entities)
    tabNames = ["A", "B", "C"]

    N = len(tabNames)
    for i, text in enumerate(tabNames):
        tabs.add(TabEntity(dimensions, text, i, N))
    return tabs

def drawPanelBackground(screen, dimensions):
    # draw panel
        x, y = dimensions.FIELD_WIDTH, 0
        width, height = dimensions.PANEL_WIDTH, dimensions.SCREEN_HEIGHT
        pygame.draw.rect(screen, (100,100,100), (x, y, width, height))

def main():
    
    # Initialize field
    dimensions = Dimensions()
    screen = dimensions.resizeScreen(800, 800)
    fieldTransform: FieldTransform = FieldTransform(dimensions)
    initReferenceframe(dimensions, fieldTransform)
    mouse: PointRef = PointRef()

    # initialize images
    images = ImageManager()
    
    # Initialize entities
    interactor = Interactor(dimensions, fieldTransform)
    entities = EntityManager()

    # initialize commands
    commandBuilder = CommandBuilder(entities, interactor, images, dimensions)

    # Create path
    path = Path(commandBuilder, entities, interactor, dimensions, PointRef(Ref.FIELD, (24,24)))

    # Create tabs
    tabs = initTabs(dimensions, entities)


    # Add permanent static entities
    entities.addEntity(StaticEntity(lambda: screen.fill((255,255,255)), drawOrder = DrawOrder.BACKGROUND))
    entities.addEntity(StaticEntity(lambda: fieldTransform.draw(screen), drawOrder = DrawOrder.FIELD_BACKGROUND))
    entities.addEntity(StaticEntity(lambda: drawPanelBackground(screen, dimensions), drawOrder = DrawOrder.PANEL_BACKGROUND))
    entities.addEntity(StaticEntity(lambda: interactor.drawSelectBox(screen), drawOrder = DrawOrder.MOUSE_SELECT_BOX))

    # initialize pygame artifacts
    pygame.display.set_caption("Pathogen 4.0 (Ansel Chang)")
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        mouse.screenRef = pygame.mouse.get_pos()
        interactor.setHoveredEntity(entities.getEntityAtPosition(mouse))

        # handle events and call callbacks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = dimensions.resizeScreen(*event.size)
                fieldTransform.resizeScreen()
            elif event.type == pygame.MOUSEWHEEL:
                fieldTransform.changeZoom(mouse, event.y * 0.1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ctrlKey = pygame.key.get_pressed()[pygame.K_LCTRL]
                shiftKey = pygame.key.get_pressed()[pygame.K_LSHIFT]
                right = (event.button == 1 and ctrlKey) or event.button == 3
                interactor.onMouseDown(entities, mouse, right, shiftKey)

            elif event.type == pygame.MOUSEBUTTONUP:
                interactor.onMouseUp(entities, mouse, path)

            elif event.type == pygame.MOUSEMOTION:
                interactor.onMouseMove(entities, mouse)

        # Perform calculations
        entities.tick()

        # Draw everything
        entities.drawEntities(interactor, screen)

        # Update display and maintain frame rate
        pygame.display.flip()
        clock.tick(60) # fps

if __name__ == "__main__":
    main()
