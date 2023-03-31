from CommandCreation.command_definition_database import CommandDefinitionDatabase
from Commands.command_block_entity import CommandBlockEntity
from Commands.custom_command_block_entity import CustomCommandBlockEntity
from Commands.command_inserter import CommandInserter
from Commands.command_expansion import CommandExpansion

from CommandCreation.command_block_entity_factory import CommandBlockEntityFactory

from NodeEntities.path_node_entity import PathNodeEntity
from SegmentEntities.path_segment_entity import PathSegmentEntity

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from Adapters.path_adapter import NullPathAdapter

from linked_list import LinkedList
from dimensions import Dimensions
from reference_frame import PointRef

"""
A class storing state for a segment and the node after it.
Also stores the relevant commands, and facilitates their interface through Adapter design pattern
"""
class Path:

    def __init__(self, database: CommandDefinitionDatabase, entities: EntityManager, interactor: Interactor, commandFactory: CommandBlockEntityFactory, commandExpansion: CommandExpansion, dimensions: Dimensions, startPosition: PointRef):
            
        self.database = database
        self.entities = entities
        self.interactor = interactor
        self.commandFactory = commandFactory
        self.commandExpansion = commandExpansion
        self.dimensions = dimensions

        self.pathList = LinkedList() # linked list of nodes and segments
        self.commandList = LinkedList() # linked list of CommandEntities

        self._addInserter(self.commandList.addToEnd) # add initial CommandInserter
        self._addRawNode(startPosition, self.commandList.addToEnd) # add start node
        self._addInserter(self.commandList.addToEnd) # add final CommandInserter
        self.recomputeY()
        self.node.updateAdapter()

    def recomputeY(self):
        self.commandList.head.updateNextY()

    def _addInserter(self, func):

        inserter = CommandInserter(self.interactor, self.dimensions, self.addCustomCommand)
        func(inserter)
        self.entities.addEntity(inserter)

    def _addRawNode(self, nodePosition: PointRef, func):

        # create node and add entity
        self.node: PathNodeEntity = PathNodeEntity(position = nodePosition)
        self.pathList.addToEnd(self.node)
        self.entities.addEntity(self.node)

        # create turn command and add entity
        self.turnCommand = self.commandFactory.create(self, self.node.getAdapter())
        func(self.turnCommand)
        self.entities.addEntity(self.turnCommand)

    def _addRawSegment(self):

        # create segment and add entity
        self.segment: PathSegmentEntity = PathSegmentEntity(self.interactor)
        self.pathList.addToEnd(self.segment)
        self.entities.addEntity(self.segment)

        # create segment command and add entity
        self.segmentCommand = self.commandFactory.create(self, self.segment.getAdapter())
        self.commandList.insertBeforeEnd(self.segmentCommand)
        self.entities.addEntity(self.segmentCommand)

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
        self.entities.addEntity(command)
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
                node.position._isExpanded = isExpand
                node.position.recomputeExpansion()
            node = node.getNext()
