from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Iterator
from command_creation.command_type import CommandType
from common.draw_order import DrawOrder

from data_structures.observer import Observer
from root_container.panel_container.command_block_section.section_entity import SectionEntity
from root_container.panel_container.element.overall.task_commands_container import TaskCommandsContainer

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
import math


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

        self.scrollHandler = CommandScrollingHandler(panel, DrawOrder.COMMANDS)
        scrollingContainer = self.scrollHandler.getScrollingContainer()
        self.vgc: VariableGroupContainer[SectionEntity] = VariableGroupContainer(scrollingContainer, isHorizontal = False, name = "main")

        self.vgc.subscribe(self, onNotify = lambda: self.scrollHandler.setContentHeight(self.vgc.HEIGHT))        

        # insert first inserter
        variableContainer = self._createInserter(self.vgc)
        self.getList(variableContainer).addToBeginning(variableContainer)

        # Create first section
        self.addSection()

    def _createSection(self) -> VariableContainer[SectionEntity]:
        vc = VariableContainer(self.vgc, isHorizontal = False)
        section = SectionEntity(vc, self)
        vc.setChild(section)
        return vc
    
    # add section to end
    def addSection(self):
        sectionVC = self._createSection()
        self.vgc.containers.addToEnd(sectionVC)
        self._insertInserterAfter(sectionVC)
    
    # add section after where section inserter is, and then insert another inserter after that
    def _insertSectionAt(self, inserter: CommandInserter):
        assert(inserter.isSectionInserter())

        inserterVC: VariableContainer = inserter._parent
        assert(self.vgc.containers.contains(inserterVC))

        sectionVC = self._createSection()
        self.vgc.containers.insertAfter(inserterVC, sectionVC)
        self._insertInserterAfter(sectionVC)

    def getList(self, commandOrInserter: CommandBlockEntity | CommandInserter = None) -> LinkedList[VariableContainer[Element]]:
        return self.getVGC(commandOrInserter).containers

    # get the mutable linked list in order to add/remove commands
    # if a variable container is passed in, get the list containing it.
    def getVGC(self, commandOrInserter: CommandBlockEntity | CommandInserter = None) -> VariableGroupContainer[Element]:
        
        # main list
        if commandOrInserter is None or self.vgc.containers.contains(commandOrInserter):
            return self.vgc
        elif isinstance(commandOrInserter, VariableContainer):
            return commandOrInserter.group
        else:
            return commandOrInserter.getVGC()
    
    def recomputePosition(self):
        print("recompute sequence handler")
        self.vgc.recomputeEntity()
    
    # Set up the command block entity and tie it to the VariableGroupContainer
    def _createCommand(self, adapter: PathAdapter, vgc: VariableGroupContainer) -> tuple[VariableContainer, CommandBlockEntity]:
        
        # Create the variable container tied to the VariableGroupContainer
        variableContainer = VariableContainer(vgc, False)

        # Create the CommandBlockContainer, which holds the CommandBlockEntity
        commandContainer = CommandBlockContainer(variableContainer)
        variableContainer.setChild(commandContainer)

        # Create the CommandBlockEntity, which is inside CommandBLockContainer, and holds the command definition
        commandBlock = self.factory.create(commandContainer, self, adapter)
        commandContainer.initCommandBlock(commandBlock)
        
        return variableContainer, commandBlock
    
    def _createInserter(self, vgc: VariableGroupContainer) -> VariableContainer:

        # create the variable container that holds the CommandInserter
        variableContainer = VariableContainer(vgc, False)

        # create the CommandInserter
        inserter = CommandInserter(variableContainer, self, onInsert = lambda inserter: self._onInsert(inserter))
        variableContainer.setChild(inserter)

        return variableContainer
    
    # Set up the inserter and tie it to the VariableGroupContainer
    def _insertInserterAfter(self, commandVariableContainer: VariableContainer) -> VariableContainer:
        vgc = self.getVGC(commandVariableContainer)
        variableContainer = self._createInserter(vgc)
        self.getList(commandVariableContainer).insertAfter(commandVariableContainer, variableContainer)

    # Insert custom command at location of inserter. Handled directly here
    # and not through path, as does not affect the path
    def insertCustomCommand(self, inserter: CommandInserter) -> CommandBlockEntity:
        return self.insertCommandAfter(inserter, NullPathAdapter())
    
    # when an inserter is clicked
    # determine whether the inserter is for a command or for a section
    def _onInsert(self, inserter: CommandInserter) -> None:
        if inserter.getVGC().name == "section" or inserter.getVGC().name == "task":
            # insert command
            self.insertCustomCommand(inserter)
        elif inserter.getVGC().name == "main":
            # insert section
            self._insertSectionAt(inserter)
        self.recomputePosition()
    
    # create and insert command at beginning of list given path adapter
    # make sure to add after the first insreter
    def insertCommandAtBeginning(self, adapter: PathAdapter, vgc: VariableGroupContainer = None) -> CommandBlockEntity:
        variableContainer, commandBlock = self._createCommand(adapter, vgc)
        self.getList().insertAfter(self.getList().head, variableContainer)
        self._insertInserterAfter(variableContainer)

        return commandBlock
    
    # create and insert command after given command block entity and path adapter
    # make sure to add after the inserter AFTER the command block
    # if after is None, add to end
    def insertCommandAfter(self, after: CommandBlockEntity | CommandInserter, adapter: PathAdapter) -> CommandBlockEntity:
        
        if after is None:
            lastSectionInserterVC: VariableContainer[SectionEntity] = self.vgc.containers.tail
            lastSection = lastSectionInserterVC.getPrevious().child
            assert(isinstance(lastSection, SectionEntity))
            vgc = lastSection.getVGC()
        else:
            vgc = self.getVGC(after)

        variableContainer, commandBlock = self._createCommand(adapter, vgc)

        if after is None:
            vgc.containers.addToEnd(variableContainer)
        else:
            if isinstance(after, CommandBlockEntity):
                inserterVariableContainer = after.container.variableContainer.getNext()
            elif isinstance(after, CommandInserter):
                inserterVariableContainer = after.container
            vgc.containers.insertAfter(inserterVariableContainer, variableContainer)

        self._insertInserterAfter(variableContainer)

        return commandBlock
        
    def deleteCommand(self, command: CommandBlockEntity):
        # remove from linked list
        self.getList(command).remove(command.container.variableContainer)

        # remove from global entities list
        command.entities.removeEntity(command.container)

        # Remove inserter as well
        inserterVariableContainer = command.container.variableContainer.getNext()
        self.getList(inserterVariableContainer).remove(inserterVariableContainer)
        command.entities.removeEntity(inserterVariableContainer)

    # move command from current location to the after inserter
    # move the inserter after the command as well
    def moveCommand(self, command: CommandBlockEntity, inserter: CommandInserter):

        oldVgc = self.getVGC(command)
        oldVgcList = self.getList(command)
        newVgc = self.getVGC(inserter)
        newVgcList = self.getList(inserter)
        assert(inserter._parent._parent is newVgc)
        print("MOVE", oldVgc.name, newVgc.name)
        print(inserter._parent)
        for inserterVC in newVgcList:
            print(inserterVC.child is inserter, inserterVC.child)
        print("child", inserter)
        print("parent", inserter._parent)
        print("gp", inserter._parent._parent)
        assert(newVgcList.contains(inserter._parent))

        commandVariableContainer = command.container.variableContainer
        
        # remove command from the current position, without deleting from entities list
        inserterVariableContainer = commandVariableContainer.getNext()
        oldVgcList.remove(commandVariableContainer)

        # Remove next inserter entirely
        assert(inserter is not inserterVariableContainer.child)
        oldVgcList.remove(inserterVariableContainer)
        command.entities.removeEntity(inserterVariableContainer)

        # insert command after the given inserter
        commandVariableContainer.changeParent(newVgc)
        newVgcList.insertAfter(inserter.container, commandVariableContainer)

        # create and insert new inserter
        self._insertInserterAfter(commandVariableContainer)
        
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
        self.vgc.recomputeEntity()
        self.forceAnimationToEnd = False
        self.scrollHandler.setContentHeight(self.vgc.HEIGHT)

    def _updateClosestInserter(self, inserter: CommandInserter, mouseY: int, closestInserter: CommandInserter, closestDistance: float) -> tuple:
        distance = abs(inserter.CENTER_Y - mouseY)
        if distance < closestDistance:
            closestDistance = distance
            closestInserter = inserter
        return closestInserter, closestDistance
    
    def insertInserterIfNotHidden(self, inserters: list[CommandInserter], inserter: CommandInserter):

        if inserter.getPreviousCommand() is not None and not inserter.getPreviousCommand().isVisible():
            return
        
        inserters.append(inserter)

    # generate a list of inserters that the user can insert a command into
    def generateActiveCommandInserters(self) -> list[CommandInserter]:
        inserters: list[CommandInserter] = []

        for sectionOrInserterVC in self.vgc.containers:

            # cannot insert into section inserters
            if not isinstance(sectionOrInserterVC.child, SectionEntity):
                continue

            section: SectionEntity = sectionOrInserterVC.child

            # cannot insert into collapsed section
            if not section.isExpanded():
                continue

            for commandOrInserterVC in section.getVGC().containers:

                # regular command inserter inside section
                if isinstance(commandOrInserterVC.child, CommandInserter):
                    self.insertInserterIfNotHidden(inserters, commandOrInserterVC.child)

                # task
                elif isinstance(commandOrInserterVC.child, CommandBlockContainer):
                    cbc: CommandBlockContainer = commandOrInserterVC.child
                    cbe: CommandBlockEntity = cbc.commandBlock
                    if cbe.isTask():
                        for commandOrInserterVC in cbe.getTaskList():
                            if isinstance(commandOrInserterVC.child, CommandInserter):
                                self.insertInserterIfNotHidden(inserters, commandOrInserterVC.child)
        return inserters
    
    def updateActiveCommandInserters(self):
        self.activeCommandInserters = self.generateActiveCommandInserters()

    # find closest inserter to mouse position.
    # if command is not custom, cannot swap order of command with other non-custom commands
    def getClosestInserter(self, mouse: tuple, command: CommandBlockEntity) -> CommandInserter | None:
        mx, my = mouse

        closestInserter = self.activeCommandInserters[0]
        closestDistance = abs(closestInserter.CENTER_Y - my)
        for inserter in self.activeCommandInserters[1:]:
            closestInserter, closestDistance = self._updateClosestInserter(inserter, my, closestInserter, closestDistance)

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
            if element.getVGC().name == "main":
                return None
            elif element.getVGC().name == "section" or element.getVGC().name == "task":
                previousVariableContainer: VariableContainer[CommandBlockContainer] = element.container.getPrevious()
                if previousVariableContainer is None:
                    return None
                else:
                    return previousVariableContainer.child.commandBlock
        else:
            print("error")
            self.vgc.tree(element)
            raise Exception("Invalid element type")
        
    def onGlobalCommandExpansionChange(self):
        self.vgc.propagateChange()

    # returns true if the inserter is the only inserter in the list (whether it is main list or task command)
    def isOnlyInserter(self, inserter: CommandInserter) -> bool:

        if inserter.isSectionInserter():
            return False

        list = self.getList(inserter)

        current = list.head
        while current is not None:
            if isinstance(current.child, CommandBlockContainer):
                if current.child.commandBlock.isVisible():
                    return False
            current = current.getNext()

        return inserter is list.head.child