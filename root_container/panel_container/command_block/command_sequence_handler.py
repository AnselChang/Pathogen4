from adapter.path_adapter import NullPathAdapter, PathAdapter
from command_creation.command_block_entity_factory import CommandBlockEntityFactory
from data_structures.linked_list import LinkedList
from entity_ui.group.variable_group.variable_container import VariableContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
from root_container.panel_container.command_block.command_block_container import CommandBlockContainer
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter
from root_container.panel_container.command_block.command_or_inserter import CommandOrInserter
from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer
from root_container.panel_container.command_scrolling.command_scrolling_handler import CommandScrollingHandler
from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
from root_container.path import Path


"""
Handles specifically the list of commands, and later command groups.
Uses a VariableGroupContainer to position the commands.

Handles scrolling and command expansion.

Whenever a command is added or deleted, the inserter after it is added/deleted as well
"""

Element = CommandOrInserter | CommandBlockContainer | CommandInserter

class CommandSequenceHandler:

    def __init__(self, panel: BlockTabContentsContainer, path: Path, factory: CommandBlockEntityFactory, commandExpansion: CommandExpansionContainer):

        self.panel = panel
        self.path = path
        self.factory = factory
        self.vgc: VariableGroupContainer[Element] = VariableGroupContainer(self)

        # On command expansion button click, recalculate targets
        self.commandExpansion = commandExpansion
        self.commandExpansion.subscribe(self, onNotify = self.vgc.propagateChange)

        self.scrollHandler = CommandScrollingHandler(panel)

        # Should be initialized with a single inserter in the beginning
        variableContainer = self._createInserter()
        self.getList().addToBeginning(variableContainer)

    # get the mutable linked list in order to add/remove commands
    def getList(self) -> LinkedList[VariableContainer[Element]]:
        return self.vgc.containers
    
    # Set up the command block entity and tie it to the VariableGroupContainer
    def _createCommand(self, adapter: PathAdapter) -> VariableContainer:
        # Create the variable container tied to the VariableGroupContainer
        variableContainer = VariableContainer(self.vgc, False)

        # Create the CommandBlockContainer, which holds the CommandBlockEntity
        commandContainer = CommandBlockContainer(variableContainer)

        # Create the CommandBlockEntity, which is inside CommandBLockContainer, and holds the command definition
        commandBlock = self.factory.create(commandContainer, self, adapter)
        
        return variableContainer
    
    def _createInserter(self) -> VariableContainer:
        # create the variable container that holds the CommandInserter
        variableContainer = VariableContainer(self.vgc, False)

        # create the CommandInserter
        inserter = CommandInserter(variableContainer, self, onInsert = lambda inserter: self.insertCustomCommand(inserter))

        return variableContainer
    
    # Set up the inserter and tie it to the VariableGroupContainer
    def _insertCommandInserterAfter(self, commandVariableContainer: VariableContainer) -> VariableContainer:
        
        variableContainer = self._createInserter()
        self.getList().insertAfter(commandVariableContainer, variableContainer)

    # Insert custom command at location of inserter. Handled directly here
    # and not through path, as does not affect the path
    def insertCustomCommand(self, inserter: CommandInserter):
        self.insertCommandAfter(inserter, NullPathAdapter())
    
    # create and insert command at beginning of list given path adapter
    def insertCommandAtBeginning(self, adapter: PathAdapter):
        self.getList().addToBeginning(self._createCommand(adapter))
        self.vgc.recomputePosition()

    # create and insert command at end of list given path adapter
    def insertCommandAtEnd(self, adapter: PathAdapter):
        self.getList().addToEnd(self._createCommand(adapter))
        self.vgc.recomputePosition()
    
    # create and insert command after given command block entity and path adapter
    def insertCommandAfter(self, after: CommandOrInserter, adapter: PathAdapter):
        self.getList().insertAfter(after.container, self._createCommand(adapter))
        self.vgc.recomputePosition()
        
    def deleteCommand(self, command: CommandBlockEntity):
        # remove from linked list
        self.getList().remove(command.container)

        # remove from global entities list
        command.entities.removeEntity(command.container)

        self.vgc.recomputePosition()
        
    # set the local expansion flag for each command to isExpand
    def setAllLocalExpansion(self, isExpand: bool):
        node: VariableContainer[Element] = self.getList().head
        while node is not None:
            maybeCommandBlock = node.child.commandBlock
            if isinstance(maybeCommandBlock, CommandBlockEntity):
                maybeCommandBlock.setLocalExpansion(isExpand)
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