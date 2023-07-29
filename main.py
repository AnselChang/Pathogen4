from common.window import Window
from entity_base.static_entity import StaticEntity
from entity_base.tick_entity import TickEntity
from entity_ui.scrollbar.scrolling_container import ScrollingContainer
from entity_ui.selector_menu.selector_menu_manager import SelectorMenuManager
from models.project_history_interface import ProjectHistoryInterface
from models.project_history_model import ProjectHistoryModel
from models.project_model import ProjectModel
from models.ui_model import UIModel
from entities.command_editor_container.command_editor_panel import CommandEditorPanel

from entities.root_container.main_window_container import MainWindowContainer

from command_creation.command_definition_database import CommandDefinitionDatabase
from command_creation.test_commands import *

from common.reference_frame import initReferenceFrame
from common.draw_order import DrawOrder
import multiprocessing as mp

import cProfile


RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]

def runCommandsWindow(isProcessDone):

    commandsWindow = Window(0.4, 0.4, 0.6, 0)
    commandsWindowContainer = CommandEditorPanel(commandsWindow.getRootContainer())

    commandsWindow.run(isProcessDone)

def main():

    # initialize project history model
    ProjectHistoryInterface.initInstance(ProjectHistoryModel())

    # Project model that stores all the state of the program
    # makes it easy to serialize and deserialize
    projectModel = ProjectModel.getInstance()
    uiModel = UIModel.getInstance()

    window = Window(0.8, 0.8, 0, 0)
    windowContainer = MainWindowContainer(window.getRootContainer(), projectModel, runCommandsWindow)

    uiModel.initRootContainer(windowContainer)

    # Initialize major components
    panelContainer = windowContainer.PANEL_CONTAINER
    fieldContainer = windowContainer.FIELD_CONTAINER
    topBarContainer = windowContainer.TOP_BAR_CONTAINER

    initReferenceFrame(window.dimensions, fieldContainer.fieldEntity)

    projectModel.initFieldEntity(fieldContainer.fieldEntity)

    # handles the creating of menus when an entity is selected
    menuManager = SelectorMenuManager(fieldContainer.fieldEntity)
    window.interactor.initInteractor(menuManager, fieldContainer.fieldEntity)


    StaticEntity(lambda: window.interactor.drawSelectBox(window.screen), drawOrder = DrawOrder.FRONT)

    # initialize commands
    database = CommandDefinitionDatabase()

    # create command model
    scrollingContainer = ScrollingContainer(panelContainer)
    projectModel.initCommandParentEntity(scrollingContainer.getContainer())
    projectModel.commandsModel.initParentUI(scrollingContainer.getContainer())

    # initialize everything
    print("compute everything")
    window.getRootContainer().recomputeEntity()

    # create first path node
    START_POSITION = (20,20)
    projectModel.pathModel.initFirstNode(START_POSITION)

    # make initial save
    ProjectHistoryInterface.getInstance().save()

    window.run()

if __name__ == "__main__":
    #cProfile.run('main()', sort='cumtime')
    main()
