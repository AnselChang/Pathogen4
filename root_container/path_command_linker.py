from command_creation.command_type import CommandType
from models.command_models.command_model import CommandModel
from root_container.field_container.node.path_node_entity import PathNodeEntity
from root_container.field_container.path_element import PathElement
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
from root_container.field_container.segment.segment_type import PathSegmentType
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

"""
In charge of linking the path entity (node or segment) from and to the command.
This is necessary for when path entities get deleted, so that the command can be deleted as well.
This is also useful for when the path entity needs to highlight the command, or vice versa.
The added complication is that one segment is linked to each segment command,
i.e. Straight, Arc, Bezier.
"""

class PathCommandLinker:

    def __init__(self):
        self.nodeToCommand: dict[PathNodeEntity, CommandModel] = {}
        self.segmentToCommand: dict[PathSegmentEntity, CommandModel] = {}

        self.commandToPath: dict[CommandModel, PathElement] = {}

    def linkNode(self, node: PathNodeEntity, command: CommandModel):
        self.nodeToCommand[node] = command
        self.commandToPath[command] = node

    def linkSegment(self, segment: PathElement, command: CommandModel):

        if segment not in self.segmentToCommand:
            self.segmentToCommand[segment] = []

        self.segmentToCommand[segment] = command
        self.commandToPath[command] = segment

    def getCommandFromPath(self, nodeOrSegment: PathElement) -> CommandModel:
        if isinstance(nodeOrSegment, PathNodeEntity):
            return self.nodeToCommand[nodeOrSegment]
        elif isinstance(nodeOrSegment, PathSegmentEntity):
            return self.segmentToCommand[nodeOrSegment]

    def getPathFromCommand(self, command: CommandModel) -> PathElement:
        return self.commandToPath[command]
    
    def deleteNode(self, node: PathNodeEntity):
        command = self.nodeToCommand[node]
        del self.nodeToCommand[node]
        del self.commandToPath[command]

    def deleteSegment(self, segment: PathSegmentEntity):
        command = self.segmentToCommand[segment]
        del self.commandToPath[command]
        del self.segmentToCommand[segment]