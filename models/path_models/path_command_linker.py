from command_creation.command_type import CommandType
from models.command_models.command_model import CommandModel, SerializedCommandState
from models.path_models.path_node_model import PathNodeModel, SerializedPathNodeState
from models.path_models.path_segment_model import PathSegmentModel, SerializedPathSegmentState
from models.path_models.path_element_model import PathElementModel, SerializedPathElementState
from entities.root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
from entities.root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from serialization.serializable import Serializable, SerializedState
from utility.pretty_printer import PrettyPrinter

"""
In charge of linking the path entity (node or segment) from and to the command.
This is necessary for when path entities get deleted, so that the command can be deleted as well.
This is also useful for when the path entity needs to highlight the command, or vice versa.
The added complication is that one segment is linked to each segment command,
i.e. Straight, Arc, Bezier.

Fully serializable, as PathNodeModel, PathSegmentModel, and CommandModel all are.
"""

class SerializedLinkerState(SerializedState):
    
    def __init__(self,
                nodeToCommand: dict[SerializedPathNodeState, SerializedCommandState],
                segmentToCommand: dict[SerializedPathSegmentState, SerializedCommandState],
                commandToPath: dict[SerializedCommandState, SerializedPathElementState],
                 ):
        self.nodeToCommand = nodeToCommand
        self.segmentToCommand = segmentToCommand
        self.commandToPath = commandToPath

class PathCommandLinker(Serializable):

    def serialize(self) -> SerializedLinkerState:
        nodeToCommand: dict[SerializedPathNodeState, SerializedCommandState] = {}
        for node, command in self.nodeToCommand.items():
            nodeToCommand[node.serialize()] = command.SERIALIZED

        segmentToCommand: dict[SerializedPathSegmentState, SerializedCommandState] = {}
        for segment, command in self.segmentToCommand.items():
            segmentToCommand[segment.serialize()] = command.SERIALIZED

        commandToPath: dict[SerializedCommandState, SerializedPathElementState] = {}
        for command, path in self.commandToPath.items():
            commandToPath[command.SERIALIZED] = path.serialize()

        return SerializedLinkerState(nodeToCommand, segmentToCommand, commandToPath)

    @staticmethod
    def deserialize(state: SerializedLinkerState) -> 'PathCommandLinker':
        
        linker = PathCommandLinker()

        for node, command in state.nodeToCommand.items():
            print("dn", node)
            print("dc", command, command.DESERIALIZED)
            linker.nodeToCommand[node.deserialize()] = command.DESERIALIZED

        for segment, command in state.segmentToCommand.items():
            linker.segmentToCommand[segment.deserialize()] = command.DESERIALIZED

        for command, path in state.commandToPath.items():
            linker.commandToPath[command.DESERIALIZED] = path.deserialize()

        return linker
        


    def __init__(self):
        self.nodeToCommand: dict[PathNodeModel, CommandModel] = {}
        self.segmentToCommand: dict[PathSegmentModel, CommandModel] = {}

        self.commandToPath: dict[CommandModel, PathElementModel] = {}

    def linkNode(self, node: PathNodeModel, command: CommandModel):
        self.nodeToCommand[node] = command
        self.commandToPath[command] = node

    def linkSegment(self, segment: PathElementModel, command: CommandModel):

        if segment not in self.segmentToCommand:
            self.segmentToCommand[segment] = []

        self.segmentToCommand[segment] = command
        self.commandToPath[command] = segment

    def getCommandFromPath(self, nodeOrSegment: PathElementModel) -> CommandModel:
        if isinstance(nodeOrSegment, PathNodeModel):
            return self.nodeToCommand[nodeOrSegment]
        elif isinstance(nodeOrSegment, PathSegmentModel):
            return self.segmentToCommand[nodeOrSegment]

    def getPathFromCommand(self, command: CommandModel) -> PathElementModel:
        return self.commandToPath[command]
    
    def deleteNode(self, node: PathNodeModel):
        command = self.nodeToCommand[node]
        del self.nodeToCommand[node]
        del self.commandToPath[command]

    def deleteSegment(self, segment: PathSegmentModel):
        command = self.segmentToCommand[segment]
        del self.commandToPath[command]
        del self.segmentToCommand[segment]