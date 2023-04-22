from __future__ import annotations
from typing import TYPE_CHECKING

from data_structures.observer import Observer

if TYPE_CHECKING:
    from root_container.path import Path
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer


from adapter.path_adapter import NullPathAdapter, PathAdapter
from command_creation.command_block_entity_factory import CommandBlockEntityFactory
from command_creation.command_definition_database import CommandDefinitionDatabase
from data_structures.linked_list import LinkedList
from entity_ui.group.variable_group.variable_container import VariableContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
from root_container.panel_container.command_block.command_block_container import CommandBlockContainer
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter
from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer
from root_container.panel_container.command_scrolling.command_scrolling_handler import CommandScrollingHandler



"""
Handles specifically the list of commands, and later command groups.
Uses a VariableGroupContainer to position the commands.

Handles scrolling and command expansion.

Whenever a command is added or deleted, the inserter after it is added/deleted as well
"""

Element =  CommandBlockContainer | CommandInserter

class CommandSequenceHandler(Observer):

    def initPath(self, path: Path):
        self.path = path

    def initCommandExpansion(self, commandExpansion: CommandExpansionContainer):
        self.commandExpansion = commandExpansion
        self.factory = CommandBlockEntityFactory(self.database, self.panel, commandExpansion)

    def __init__(self, panel: BlockTabContentsContainer, database: CommandDefinitionDatabase):

        self.panel = panel
        self.database = database

        self.scrollHandler = CommandScrollingHandler(panel)
        scrollingContainer = self.scrollHandler.getScrollingContainer()
        self.vgc: VariableGroupContainer[Element] = VariableGroupContainer(scrollingContainer, isHorizontal = False)

        self.vgc.subscribe(self, onNotify = lambda: self.scrollHandler.setContentHeight(self.vgc.HEIGHT))        

        # Should be initialized with a single inserter in the beginning
        variableContainer = self._createInserter()
        self.getList().addToBeginning(variableContainer)

    # get the mutable linked list in order to add/remove commands
    def getList(self) -> LinkedList[VariableContainer[Element]]:
        return self.vgc.containers
    
    def recomputePosition(self):
        self.vgc.recomputePosition()
    
    # Set up the command block entity and tie it to the VariableGroupContainer
    def _createCommand(self, adapter: PathAdapter) -> tuple[VariableContainer, CommandBlockEntity]:
        # Create the variable container tied to the VariableGroupContainer
        variableContainer = VariableContainer(self.vgc, False)

        # Create the CommandBlockContainer, which holds the CommandBlockEntity
        commandContainer = CommandBlockContainer(variableContainer)
        variableContainer.setChild(commandContainer)

        # Create the CommandBlockEntity, which is inside CommandBLockContainer, and holds the command definition
        commandBlock = self.factory.create(commandContainer, self, adapter)
        commandContainer.initCommandBlock(commandBlock)
        
        return variableContainer, commandBlock
    
    def _createInserter(self) -> VariableContainer:
        # create the variable container that holds the CommandInserter
        variableContainer = VariableContainer(self.vgc, False)

        # create the CommandInserter
        inserter = CommandInserter(variableContainer, self, onInsert = lambda inserter: self._onInsert(inserter))
        variableContainer.setChild(inserter)

        return variableContainer
    
    # Set up the inserter and tie it to the VariableGroupContainer
    def _insertCommandInserterAfter(self, commandVariableContainer: VariableContainer) -> VariableContainer:
        
        variableContainer = self._createInserter()
        self.getList().insertAfter(commandVariableContainer, variableContainer)

    # Insert custom command at location of inserter. Handled directly here
    # and not through path, as does not affect the path
    def insertCustomCommand(self, inserter: CommandInserter) -> CommandBlockEntity:
        return self.insertCommandAfter(inserter, NullPathAdapter())
    
    # version of insertCustomCommand without return for onClick lambda
    def _onInsert(self, inserter: CommandInserter) -> None:
        self.insertCustomCommand(inserter)
        self.recomputePosition()
    
    # create and insert command at beginning of list given path adapter
    # make sure to add after the first insreter
    def insertCommandAtBeginning(self, adapter: PathAdapter) -> CommandBlockEntity:
        variableContainer, commandBlock = self._createCommand(adapter)
        self.getList().insertAfter(self.getList().head, variableContainer)
        self._insertCommandInserterAfter(variableContainer)

        return commandBlock
    
    # create and insert command after given command block entity and path adapter
    # make sure to add after the inserter AFTER the command block
    # if after is None, add to end
    def insertCommandAfter(self, after: CommandBlockEntity, adapter: PathAdapter) -> CommandBlockEntity:
        variableContainer, commandBlock = self._createCommand(adapter)

        if after is None:
            self.getList().addToEnd(variableContainer)
        else:
            if isinstance(after, CommandBlockEntity):
                inserterVariableContainer = after.container.variableContainer.getNext()
            else:
                inserterVariableContainer = after.container
            self.getList().insertAfter(inserterVariableContainer, variableContainer)

        self._insertCommandInserterAfter(variableContainer)

        return commandBlock
        
    def deleteCommand(self, command: CommandBlockEntity):
        # remove from linked list
        self.getList().remove(command.container.variableContainer)

        # remove from global entities list
        command.entities.removeEntity(command.container)

        # Remove inserter as well
        inserterVariableContainer = command.container.variableContainer.getNext()
        self.getList().remove(inserterVariableContainer)
        command.entities.removeEntity(inserterVariableContainer)

    # move command from current location to the after inserter
    # move the inserter after the command as well
    def moveCommand(self, command: CommandBlockEntity, inserter: CommandInserter):

        commandVariableContainer = command.container.variableContainer
        
        # remove command from the current position, without deleting from entities list
        self.getList().remove(commandVariableContainer)

        # Remove next inserter entirely
        inserterVariableContainer = commandVariableContainer.getNext()
        self.getList().remove(inserterVariableContainer)
        command.entities.removeEntity(inserterVariableContainer)

        # insert command after the given inserter
        self.getList().insertAfter(inserter.container, commandVariableContainer)

        # create and insert new inserter
        self._insertCommandInserterAfter(commandVariableContainer)
        
    # set the local expansion flag for each command to isExpand
    def setAllLocalExpansion(self, isExpand: bool):
        node: VariableContainer[Element] = self.getList().head
        while node is not None:
            maybeCommandContainer = node.child
            if isinstance(maybeCommandContainer, CommandBlockContainer):
                maybeCommandContainer.commandBlock.setLocalExpansion(isExpand)
            node = node.getNext()

    def scrollToCommand(self, command: CommandBlockEntity):
        pass

    def highlightPathFromCommand(self, command: CommandBlockEntity):
        pathEntity = self.path.getPathEntityFromCommand(command)
        command.interactor.removeAllEntities()
        command.interactor.addEntity(pathEntity)

    def onWindowResize(self):

        self.forceAnimationToEnd = True
        self.vgc.recomputePosition()
        self.forceAnimationToEnd = False
        self.scrollHandler.setContentHeight(self.vgc.HEIGHT)

    # When dragging a custom command. Gets the closest inserter object to the mouse
    def getClosestInserter(self, mouse: tuple) -> CommandInserter:

        mx, my = mouse

        element: VariableContainer[Element] = self.getList().head

        closestInserter = element.child
        closestDistance = abs(closestInserter.CENTER_Y - my)
        while element is not None:

            if isinstance(element.child, CommandInserter):

                inserter = element.child
                distance = abs(inserter.CENTER_Y - my)
                if distance < closestDistance:
                    closestDistance = distance
                    closestInserter = inserter

            element = element.getNext()

        return closestInserter
    
    # # if command, gives next inserter. If next inserter, gives next command
    def getNext(self, element: Element) -> Element:

        if isinstance(element, CommandBlockEntity):
            nextVariableContainer: VariableContainer[CommandInserter] = element.container.variableContainer.getNext()
            if nextVariableContainer is None:
                return None
            else:
                return nextVariableContainer.child
        elif isinstance(element, CommandInserter):
            nextVariableContainer: VariableContainer[CommandBlockContainer] = element.container.getNext()
            if nextVariableContainer is None:
                return None
            else:
                return nextVariableContainer.child.commandBlock
        else:
            raise Exception("Invalid element type")
        
    def getPrevious(self, element: Element) -> Element:

        if isinstance(element, CommandBlockEntity):
            previousVariableContainer: VariableContainer[CommandInserter] = element.container.variableContainer.getPrevious()
            if previousVariableContainer is None:
                return None
            else:
                return previousVariableContainer.child
        elif isinstance(element, CommandInserter):
            previousVariableContainer: VariableContainer[CommandBlockContainer] = element.container.getPrevious()
            if previousVariableContainer is None:
                return None
            else:
                return previousVariableContainer.child.commandBlock
        else:
            raise Exception("Invalid element type")
        
    def onGlobalCommandExpansionChange(self):
        self.vgc.propagateChange()