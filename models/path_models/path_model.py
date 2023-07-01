"""
The path model consists of a linked list of nodes and segments.
It is in charge of storing all the path state.
In creating new nodes, it also creates the relevant command models and links them to the nodes.
"""

from data_structures.linked_list import LinkedList
from models.command_models.command_model import CommandModel
from models.path_models.path_node_model import PathNodeModel
from models.path_models.path_segment_model import PathSegmentModel
from root_container.field_container.field_entity import FieldEntity
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
from models.path_models.path_command_linker import PathCommandLinker
from serialization.serializable import Serializable, SerializedState

class SerializedPathModel(SerializedState):
    def __init__(self, pathList: LinkedList[PathNodeModel | PathSegmentEntity], linker: PathCommandLinker):
        self.pathList = pathList
        self.linker = linker

class PathModel(Serializable):

    def __init__(self):

        self.pathList = LinkedList[PathNodeModel | PathSegmentEntity]() # linked list of nodes and segments

        # store a dict that maintains a mapping from PathNodeEntity | PathSegmentEntity to CommandBlockEntity
        self.linker = PathCommandLinker()

        self.commandsModel = None
        self.fieldEntity: FieldEntity = None

    def serialize(self) -> SerializedState:
        return SerializedPathModel(self.pathList, self.linker)
    
    def deserialize(state: SerializedPathModel) -> 'PathModel':
        model = PathModel()
        model.pathList = state.pathList
        model.linker = state.linker
        return model

    def initCommandsModel(self, commandsModel: CommandModel):
        self.commandsModel = commandsModel

    def initFieldEntity(self, fieldEntity: FieldEntity):
        self.fieldEntity = fieldEntity

    def initFirstNode(self, startPosition: tuple):

        # initialize first node
        self._addRawNode(startPosition) # add start node

    def _addRawNode(self, nodePosition: tuple, afterPath = None, afterCommand: CommandModel = None, isTemporary: bool = False):

        if afterPath is None:
            afterPath = self.pathList.tail
        if afterCommand is None:
            afterCommand = self.commandsModel.getLastChild().getLastChild()

        # create node and add entity
        node: PathNodeModel = PathNodeModel(self, nodePosition, isTemporary)
        self.pathList.insertAfter(afterPath, node)

        turnCommand = CommandModel(node.getAdapter())
        if afterCommand is None:
            self.commandsModel.getLastChild().insertChildAtEnd(turnCommand)
        else:
            afterCommand.insertAfterThis(turnCommand)
        self.linker.linkNode(node, turnCommand)

        return node
    
    def _addRawNodeToBeginning(self, nodePosition: tuple, isTemporary: bool = False):

        # create node and add entity
        node: PathNodeModel = PathNodeModel(self, nodePosition, isTemporary)
        self.pathList.addToBeginning(node)

        turnCommand = CommandModel(node.getAdapter())
        self.commandsModel.getFirstChild().insertChildAtBeginning(turnCommand)
        self.linker.linkNode(node, turnCommand)

        return node


    def _addRawSegment(self, afterPath = None, afterCommand: CommandModel = None):

        if afterPath is None:
            afterPath = self.pathList.tail
        if afterCommand is None:
            afterCommand = self.commandsModel.getLastChild().getLastChild()

        # create segment and add entity
        segment: PathSegmentModel = PathSegmentModel(self)
        self.pathList.insertAfter(afterPath, segment)

        segmentCommand = CommandModel(segment.getAdapter())
        if afterCommand is None:
            self.commandsModel.getLastChild().insertChildAtEnd(segmentCommand)
        else:
            afterCommand.insertAfterThis(segmentCommand)
        self.linker.linkSegment(segment, segmentCommand)

        return segment

    # adds segment and node to the end of the path
    # return the created PathNodeEntity
    def addNode(self, nodePosition: tuple, isTemporary: bool = False) -> PathNodeModel:
        
        print("addNode")
        
        segment = self._addRawSegment()
        node = self._addRawNode(nodePosition, isTemporary = isTemporary)

        node.recomputeUI()
        self.commandsModel.ui.recomputeEntity()

        return node
    
    # insert node to split up given segment
    def insertNode(self, segment: PathSegmentEntity, position: tuple, isTemporary: bool = False) -> PathNodeModel:
        previousCommand = self.linker.getCommandFromPath(segment)
        node = self._addRawNode(position, segment, previousCommand, isTemporary = isTemporary)
        
        command = self.linker.getCommandFromPath(node)
        newSegment = self._addRawSegment(node, command)

        self.commandsModel.recomputeUI()
        node.updateAdapter()
        
        node.getNext().onNodeMove(node)
        node.getPrevious().onNodeMove(node)

        return node
    
    # insert a node and segment at the beginning of the path
    def addNodeToBeginning(self, position: tuple, isTemporary: bool = False) -> PathNodeModel:
        node = self._addRawNodeToBeginning(position, isTemporary = isTemporary)
        
        command = self.linker.getCommandFromPath(node)
        segment = self._addRawSegment(node, command)

        self.commandsModel.recomputeUI()
        node.updateAdapter()
        
        node.getNext().onNodeMove(node)

        return node
    
    # Removing a node involves removing a node and a neighboring segment
    def removeNode(self, node: PathNodeModel):

        # remove the node
        self.pathList.remove(node)
        self.entities.removeEntity(node)

        turnCommand = self.linker.getCommandFromPath(node)
        turnCommand.delete()
        
        self.commandsModel.recomputeUI()

        # remove the next segment, unless its the last segment, in which case remove the previous segment
        if node.isLastNode():
            segment = node.getPrevious()
            otherSegment = node.getNext()
        else:
            segment = node.getNext()
            otherSegment = node.getPrevious()
        
        self.pathList.remove(segment)
        self.entities.removeEntity(segment)

        segmentCommand = self.linker.getCommandFromPath(segment)
        segmentCommand.delete()
        
        # the other segment is the only node/segment affected by this
        if otherSegment is not None: # it's none if there are only two nodes total and remove last one
            otherSegment.updateAdapter()
            otherSegment.recomputePosition()

        if node.getNext() is not None:
            node.getNext().getNext().onAngleChange()
        if node.getPrevious() is not None:
            node.getPrevious().getPrevious().onAngleChange()


    def getPathEntityFromCommand(self, command: CommandModel) -> PathSegmentEntity | PathNodeModel:
        return self.linker.getPathFromCommand(command)
    
    def getCommandFromPathEntity(self, pathEntity: PathSegmentEntity | PathNodeModel) -> CommandModel:
        return self.linker.getCommandFromPath(pathEntity)
    
    # when the segment type has changed, show the correct command and hide the others
    def onSegmentTypeChange(self, segment: PathSegmentEntity, oldType, newType):
        segmentCommand = self.linker.getCommandFromPath(segment)
        segmentCommand.setNewAdapter(segment.getAdapter())
        segmentCommand.rebuild()
        self.commandsModel.recomputeUI()