from entity_base.entity import Entity
from entity_base.static_entity import StaticEntity
from entity_base.entity import initEntityClass, setRootContainer
from entity_ui.dropdown.dropdown_container import DropdownContainer
from entity_ui.group.variable_group.variable_container import VariableContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
from entity_ui.scrollbar.scrolling_container import ScrollingContainer
from entity_ui.selector_menu.selector_menu_manager import SelectorMenuManager
from models.command_models.full_model import FullModel
from models.project_model import ProjectModel
from models.ui_model import UIModel

from root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter

from entity_handler.entity_manager import EntityManager
from entity_handler.interactor import Interactor

from command_creation.command_definition_database import CommandDefinitionDatabase
from command_creation.test_commands import *
from command_creation.command_block_entity_factory import CommandBlockEntityFactory

from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer

from root_container.panel_container.panel_container import PanelContainer
from root_container.field_container.field_container import FieldContainer

from entity_ui.tooltip import initTooltipFont

from common.font_manager import FontManager, FontID
from common.image_manager import ImageManager, ImageID
from common.reference_frame import PointRef, Ref, initReferenceframe, VectorRef
from root_container.field_container.field_entity import FieldEntity
from common.dimensions import Dimensions
from common.draw_order import DrawOrder
from root_container.top_bar_container.top_bar_container import TopBarContainer
from utility.pygame_functions import getGradientSurface
from utility.math_functions import isInsideBox2
import pygame, random, threading, time, json
import sys

import cProfile


pygame.init()
pygame.key.set_repeat(400, 70)

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]

def instanceOfClasses(entity, *classes):
    for c in classes:
        if isinstance(entity, c):
            return True
    return False

# Define the I/O handling function
def io_handler(database: CommandDefinitionDatabase, model: ProjectModel, entities: EntityManager):
    while True:
        cmd = input("Enter some text: ")
        
        if cmd == "json":
            commandJSON: dict = database.exportToJson()
            print(json.dumps(commandJSON, indent = 4))
        elif cmd == "model":
            model.commandsModel.tree()
        elif cmd == "ui":
            model.commandsModel.getExistingUI().tree(verbose=False)
        elif cmd == "cmd":
            print([e for e in entities.entities if isinstance(e, CommandBlockEntity)])
        elif cmd == "path":
            model.pathModel.pathList.printList()

def main():

    # Project model that stores all the state of the program
    # makes it easy to serialize and deserialize
    projectModel = ProjectModel.getInstance()
    uiModel = UIModel.getInstance()

    # Initialize field
    dimensions = Dimensions()
    fontManager = FontManager(dimensions)
    screen = dimensions.resizeScreen(dimensions.DEFAULT_SCREEN_WIDTH, dimensions.DEFAULT_SCREEN_HEIGHT)

    images = ImageManager()
    imageSize = images.get(ImageID.FIELD).get_width()
    dimensions.setFieldSizePixels(imageSize)

    
    initTooltipFont(fontManager.getDynamicFont(FontID.FONT_NORMAL, 10))
    
    # Initialize entities
    interactor = Interactor(dimensions)
    entities = EntityManager()
    initEntityClass(entities, interactor, images, fontManager, dimensions)
    rootContainer = entities.initRootContainer()
    setRootContainer(rootContainer)

    uiModel.initRootContainer(rootContainer)


    rootContainer.initComponents(projectModel)

    # Initialize major components
    panelContainer = rootContainer.PANEL_CONTAINER
    fieldContainer = rootContainer.FIELD_CONTAINER
    topBarContainer = rootContainer.TOP_BAR_CONTAINER

    initReferenceframe(dimensions, fieldContainer.fieldEntity)
    projectModel.pathModel.initFieldEntity(fieldContainer.fieldEntity)
    fieldContainer.fieldEntity.initPathModel(projectModel.pathModel)

    # handles the creating of menus when an entity is selected
    menuManager = SelectorMenuManager(fieldContainer.fieldEntity)
    interactor.initInteractor(menuManager, fieldContainer.fieldEntity)


    StaticEntity(lambda: interactor.drawSelectBox(screen), drawOrder = DrawOrder.FRONT)

    # initialize commands
    database = CommandDefinitionDatabase()

    # create command model
    scrollingContainer = ScrollingContainer(panelContainer)
    projectModel.commandsModel.initParentUI(scrollingContainer.getContainer())


    # initialize pygame artifacts
    pygame.display.set_caption("Pathogen 4.0 (Ansel Chang)")
    clock = pygame.time.Clock()

    # initialize everything
    print("compute everything")
    rootContainer.recomputeEntity()

    # create first path node
    START_POSITION = (20,20)
    projectModel.pathModel.initFirstNode(START_POSITION)

    # Create a new thread for the I/O handling function
    io_thread = threading.Thread(target=io_handler, args = (database,projectModel,entities,), daemon=True)

    # Start the I/O handling thread
    io_thread.start()

    # Main game loop
    print("start loop")
    while True:

        dimensions.RESIZED_THIS_FRAME = False

        mouse = pygame.mouse.get_pos()
        
        hoveredEntity = entities.getEntityAtPosition(mouse)

        if hoveredEntity is not None:
            parent = f", {str(hoveredEntity._parent)}"
        else:
            parent = ""
        msg = f"({mouse[0]}, {mouse[1]}), {str(hoveredEntity)}" + parent
        #inches = fieldContainer.fieldEntity.mouseToInches(mouse)
        #mouse2 = fieldContainer.fieldEntity.inchesToMouse(inches)
        pygame.display.set_caption(msg)

        interactor.setHoveredEntity(hoveredEntity, mouse)
        # handle events and call callbacks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = dimensions.resizeScreen(*event.size)
            elif event.type == pygame.MOUSEWHEEL:
                interactor.onMouseWheel(event.y, mouse)
            elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                ctrlKey = pygame.key.get_pressed()[pygame.K_LCTRL]
                shiftKey = pygame.key.get_pressed()[pygame.K_LSHIFT]
                right = (event.button == 1 and ctrlKey) or event.button == 3
                interactor.onMouseDown(entities, mouse, right, shiftKey)

            elif event.type == pygame.MOUSEBUTTONUP:
                interactor.onMouseUp(entities, mouse)

            elif event.type == pygame.MOUSEMOTION:
                interactor.onMouseMove(entities, mouse)
            elif event.type == pygame.KEYDOWN:
                entities.onKeyDown(event.key)
            elif event.type == pygame.KEYUP:
                entities.onKeyUp(event.key)

        # Perform calculations
        entities.tick()

        # Draw everything
        entities.drawEntities(interactor, screen, mouse, dimensions)

        # Update display and maintain frame rate
        pygame.display.flip()
        clock.tick(60) # fps
        #print(clock.get_fps())

if __name__ == "__main__":
    #cProfile.run('main()', sort='cumtime')
    main()
