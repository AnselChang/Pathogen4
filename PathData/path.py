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

        self.commands = LinkedList()

        self.addNode(startPosition)

    def addNode(self, nodePosition: PointRef):
        
        # create node and add entity
        self.node: PathNodeEntity = PathNodeEntity(self, position = nodePosition)
        self.entities.addEntity(self.node)

        # create turn command and add entity
        self.turnCommand = self.commandBuilder.buildCommand(self.node.getAdapter())
        self.entities.addEntity(self.turnCommand)
        self.commands.addToEnd(self.turnCommand)

    def addNodeSection(self, nodePosition: PointRef):
                
        if self.previous is None:

            self.segment = None
            self.segmentCommand = None

        else:
            
            self.previous.next = self

            # create segment and add entity
            self.segment: PathSegmentEntity = PathSegmentEntity(self, interactor, self.previous.node, self.node)
            entities.addEntity(self.segment)

            # create turn command and add entity
            self.segmentCommand = commandBuilder.buildCommand(self.segment.getAdapter())
            self.commands.insert(0, self.segmentCommand)

            self.node.prevSegment = self.segment
            self.previous.node.nextSegment = self.segment

            self.segment.updateAdapter()

        self.node.updateAdapter()

    # recursively iterate to last section and add
    def addSectionAtEnd(self, nodePosition: PointRef):
        if self.next is None:
            self.next = PathSection(self, self.commandBuilder, self.entities, self.interactor, nodePosition)
        else:
            self.next.addSectionAtEnd(nodePosition)

    def changeSegmentShape(self, segmentAdapter: Adapter):

        state = self.commandBuilder.buildCommandState(segmentAdapter)
        self.segmentCommand.setState(state)
        

    def addInlineTurn(self, inlineTurnAdapter: TurnAdapter):
        inlineTurnCommand = self.commandBuilder.buildCommand(inlineTurnAdapter)
        self.inlineTurnCommands.append(inlineTurnCommand)

        turnCommandIndex = self.commands.index(self.turnCommand)
        self.commands.insert(turnCommandIndex, inlineTurnCommand)

    def removeInlineTurn(self):
        self.commands.remove(self.inlineTurnCommands[-1])
        del self.inlineTurnCommands[-1]

    # return string of entire list of commands for whole path (recursively expands next section)
    def __str__(self) -> str:
        string = ""
        for command in self.commands:
            string += str(command) + "\n"
        
        if self.next is not None:
            string += str(self.next)

        return string
    
    

    