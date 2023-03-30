from CommandCreation.command_builder import CommandBuilder
from Commands.command_block_entity import CommandBlockEntity

from CommandCreation.command_type import CommandType

from NodeEntities.path_node_entity import PathNodeEntity
from SegmentEntities.path_segment_entity import PathSegmentEntity
from SegmentEntities.path_segment_state import PathSegmentState

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from Adapters.adapter import Adapter
from Adapters.turn_adapter import TurnAdapter
from Adapters.straight_adapter import StraightAdapter

from linked_list import LinkedList

from reference_frame import PointRef

"""
A class storing state for a segment and the node after it.
Also stores the relevant commands, and facilitates their interface through Adapter design pattern
"""
class Path:

    def __init__(self, commandBuilder: CommandBuilder, entities: EntityManager, interactor: Interactor, startPosition: PointRef):
            
        self.commandBuilder = commandBuilder
        self.entities = entities
        self.interactor = interactor

        self.pathList = LinkedList() # linked list of nodes and segments
        self.commandList = LinkedList() # linked list of CommandEntities

        self._addRawNode(startPosition)

    def _addRawNode(self, nodePosition: PointRef):

        # create node and add entity
        self.node: PathNodeEntity = PathNodeEntity(position = nodePosition)
        self.pathList.addToEnd(self.node)
        self.entities.addEntity(self.node)

        # create turn command and add entity
        self.turnCommand = self.commandBuilder.buildCommand(self.node.getAdapter())
        self.commandList.addToEnd(self.turnCommand)
        self.entities.addEntity(self.turnCommand)
        self.turnCommand.initPosition()

    def _addRawSegment(self):

        # create segment and add entity
        self.segment: PathSegmentEntity = PathSegmentEntity(self.interactor)
        self.pathList.addToEnd(self.segment)
        self.entities.addEntity(self.segment)

        # create segment command and add entity
        self.segmentCommand = self.commandBuilder.buildCommand(self.segment.getAdapter())
        self.commandList.addToEnd(self.segmentCommand)
        self.entities.addEntity(self.segmentCommand)
        self.segmentCommand.initPosition()

    def addNode(self, nodePosition: PointRef):

        self._addRawSegment()
        self._addRawNode(nodePosition)

        self.segment.updateAdapter()
        self.node.updateAdapter()

    def changeSegmentShape(self, segmentAdapter: Adapter):

        state = self.commandBuilder.buildCommandState(segmentAdapter)
        self.segmentCommand.setState(state)

    
    

    