from command_creation.command_definition_database import CommandDefinitionDatabase
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter
from root_container.panel_container.command_expansion.command_expansion_handler import CommandExpansionHandler

from command_creation.command_block_entity_factory import CommandBlockEntityFactory

from root_container.field_container.node.path_node_entity import PathNodeEntity
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
from root_container.panel_container.panel_container import PanelContainer
from root_container.panel_container.command_scrolling.command_scrolling_handler import CommandScrollingHandler

from entity_handler.entity_manager import EntityManager
from entity_handler.interactor import Interactor

from adapter.path_adapter import NullPathAdapter

from data_structures.linked_list import LinkedList
from common.dimensions import Dimensions
from common.reference_frame import PointRef

"""
A class storing state for a segment and the node after it.
Also stores the relevant commands, and facilitates their interface through Adapter design pattern
"""
class Path:

    def __init__(self,
                 panel: PanelContainer,
                 database: CommandDefinitionDatabase,
                 entities: EntityManager,
                 interactor: Interactor,
                 commandFactory: CommandBlockEntityFactory,
                 commandExpansion: CommandExpansionHandler,
                 dimensions: Dimensions,
                 startPosition: PointRef):
            
        self.database = database
        self.entities = entities
        self.interactor = interactor
        self.commandFactory = commandFactory
        self.commandExpansion = commandExpansion
        self.dimensions = dimensions

        self.pathList = LinkedList[PathNodeEntity | PathSegmentEntity]() # linked list of nodes and segments
        self.commandList = LinkedList[CommandBlockEntity | CommandInserter]() # linked list of CommandEntities

        self.scrollHandler = CommandScrollingHandler(panel)

        # initialize first node
        self._addInserter(self.commandList.addToEnd) # add initial CommandInserter
        self._addRawNode(startPosition, self.commandList.addToEnd) # add start node
        self._addInserter(self.commandList.addToEnd) # add final CommandInserter

        self.node.updateAdapter()

        self.shouldRecomputeY = True

    # called every tick, specifically AFTER all the target heights for commands/inserters are computed
    def onTick(self):
        if self.shouldRecomputeY:
            self._recomputeY()
            self.shouldRecomputeY = False

    # Should not be directly called by commands / inserters
    # Instead, call onChangeInCommandPositionOrHeight(), which sets the recompute flag to true
    # This way, recomputation only happens a maximum of once per tick
    def _recomputeY(self):
        self.scrollHandler.setContentHeight(self.getTotalCommandHeight())
        self.commandList.head.recomputePosition()

    # call this every time position or height changes. O(1), call as many time as you want
    def onChangeInCommandPositionOrHeight(self):
        self.shouldRecomputeY = True

    def _addInserter(self):

        if self.commandList.tail is None:
            parent = self.scrollHandler.getScrollingContainer()
        else:
            parent = self.commandList.tail
        inserter = CommandInserter(parent, self, self.addCustomCommand)
        self.commandList.addToEnd(inserter)

    def _addRawNode(self, nodePosition: PointRef, func):

        # create node and add entity
        self.node: PathNodeEntity = PathNodeEntity(self.entities, self.interactor, self.dimensions, position = nodePosition)
        self.pathList.addToEnd(self.node)

        # create turn command and add entity
        self.turnCommand = self.commandFactory.create(self, self.node.getAdapter())
        self.commandList.addToEnd(self.turnCommand)

    def _addRawSegment(self):

        # create segment and add entity
        self.segment: PathSegmentEntity = PathSegmentEntity()
        self.pathList.addToEnd(self.segment)

        # create segment command and add entity
        self.segmentCommand = self.commandFactory.create(self, self.segment.getAdapter())
        self.commandList.insertBeforeEnd(self.segmentCommand)

    def addNode(self, nodePosition: PointRef):
        self._addInserter(self.commandList.addToEnd)
        self._addRawSegment()
        self._addInserter(self.commandList.addToEnd)
        self._addRawNode(nodePosition, self.commandList.insertBeforeEnd)

        self.recomputeY()
        self.segment.updateAdapter()
        self.node.updateAdapter()

    # add custom command where inserter is
    def addCustomCommand(self, inserter: CommandInserter):
        # add the custom command after the inserter
        command = self.commandFactory.create(self, NullPathAdapter())
        self.commandList.insertAfter(inserter, command)
        self._addInserter(lambda newInserter: self.commandList.insertAfter(command, newInserter))

        self.recomputeY()

    def deleteCustomCommand(self, command: CustomCommandBlockEntity):

        # remove the inserter after the command
        self.entities.removeEntity(command.getNext())
        self.commandList.remove(command.getNext())

        # remove the command
        self.commandList.remove(command)
        self.entities.removeEntity(command)
        self.recomputeY()

    # set the local expansion flag for each command to isExpand
    def setAllLocalExpansion(self, isExpand: bool):
        node: CommandBlockEntity = self.commandList.head
        while node is not None:
            if isinstance(node, CommandBlockEntity):
                node.setLocalExpansion(isExpand)
            node = node.getNext()

    # get the height of all the commands + inserters, etc. useful for scrollbar
    def getTotalCommandHeight(self) -> float:
        height = 0
        node: CommandBlockEntity | CommandInserter = self.commandList.head

        while node is not None:
            height += node.defineHeight()
            node = node.getNext()
        
        return height

    def getScrollbarOffset(self) -> int:
        return self.scrollbar.getOffset()
    
    # When dragging a custom command. Gets the closest inserter object to the mouse
    def getClosestInserter(self, mouse: PointRef) -> CommandInserter | None:

        mx, my = mouse.screenRef

        closestInserter: CommandInserter = self.commandList.head
        closestDistance = abs(closestInserter.getY() - my)

        inserter: CommandInserter = self.commandList.head
        while inserter is not None:
            if isinstance(inserter, CommandInserter):

                distance = abs(inserter.getY() - my)
                if distance < closestDistance:
                    closestDistance = distance
                    closestInserter = inserter
            inserter = inserter.getNext()

        return closestInserter
    
    def invokeEveryCommand(self, func = lambda command: None):
        command: CommandBlockEntity = self.commandList.head
        while command is not None:
            if isinstance(command, CommandBlockEntity):
                func(command)
            command = command.getNext()