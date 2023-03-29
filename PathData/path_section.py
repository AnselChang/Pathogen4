from BaseCommand.segment_command import SegmentCommand
from BaseCommand.straight_command import StraightCommand
from BaseCommand.arc_command import ArcCommand
from BaseCommand.turn_command import TurnCommand

from NodeEntities.path_node_entity import PathNodeEntity
from SegmentEntities.path_segment_entity import PathSegmentEntity
from SegmentEntities.path_segment_state import PathSegmentState

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from Adapters.adapter import SegmentAdapter
from Adapters.turn_adapter import TurnAdapter
from Adapters.straight_adapter import StraightAdapter

from reference_frame import PointRef

"""
A class storing state for a segment and the node after it.
Also stores the relevant commands, and facilitates their interface through Adapter design pattern
"""
class PathSection:

    def __init__(self, previous: 'PathSection', entities: EntityManager, interactor: Interactor, nodePosition: PointRef):

        self.previous = previous
        self.next: PathSection = None
            

        self.entities = entities
        self.interactor = interactor

        self.node: PathNodeEntity = PathNodeEntity(self, position = nodePosition)
        entities.addEntity(self.node)
        
        self.inlineTurnCommands: list[TurnCommand]
        self.turnCommand: TurnCommand = TurnCommand(self.node.getAdapter())

        self.commands = [self.turnCommand]

        if self.previous is None:

            self.segment = None
            self.segmentCommand = None

        else:
            
            self.previous.next = self

            self.segment: PathSegmentEntity = PathSegmentEntity(self, interactor, self.previous.node, self.node)
            entities.addEntity(self.segment)

            self.segmentCommand: SegmentCommand = StraightCommand(self.segment.getAdapter())
            self.commands.insert(0, self.segmentCommand)

            self.node.prevSegment = self.segment

    # recursively iterate to last section and add
    def addSectionAtEnd(self, nodePosition: PointRef):
        if self.next is None:
            self.next = PathSection(self, self.entities, self.interactor, nodePosition)
        else:
            self.next.addSectionAtEnd(nodePosition)

    def changeSegmentShape(self, segmentAdapter: SegmentAdapter):
        if segmentAdapter.id == SegmentAdapter.ID.STRAIGHT:
            self.segmentCommand = StraightCommand(segmentAdapter)
        elif segmentAdapter.id == SegmentAdapter.ID.ARC:
            self.segmentCommand = ArcCommand(segmentAdapter)

        self.commands[0] = self.segmentCommand # self.segmentCommand redefined, so update list
        

    def addInlineTurn(self, inlineTurnAdapter: TurnAdapter):
        inlineTurnCommand = TurnCommand(inlineTurnAdapter)
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
    
    

    