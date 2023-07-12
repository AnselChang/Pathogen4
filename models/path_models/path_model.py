"""
The path model consists of a linked list of nodes and segments.
It is in charge of storing all the path state.
In creating new nodes, it also creates the relevant command models and links them to the nodes.
"""

from data_structures.linked_list import LinkedList
from models.command_models.command_model import CommandModel
from models.command_models.full_model import FullCommandsModel
from models.path_models.constraint_model import ConstraintModel, SerializedConstraintsState
from models.path_models.path_element_model import SerializedPathElementState
from models.path_models.path_node_model import PathNodeModel
from models.path_models.path_segment_model import PathSegmentModel
from entities.root_container.field_container.field_entity import FieldEntity
from entities.root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
from models.path_models.path_command_linker import PathCommandLinker, SerializedLinkerState
from serialization.serializable import Serializable, SerializedState

class SerializedPathState(SerializedState):
    def __init__(self,
                 pathList: list[SerializedPathElementState],
                 linker: SerializedLinkerState,
                 constraints: SerializedConstraintsState,
                 ):
        self.pathList = pathList
        self.linker = linker
        self.constraints = constraints

class PathModel(Serializable):

    def __init__(self):

        self.pathList = LinkedList[PathNodeModel | StraightSegmentEntity]() # linked list of nodes and segments

        # store a dict that maintains a mapping from PathNodeEntity | PathSegmentEntity to CommandBlockEntity
        self.linker = PathCommandLinker()

        # Store path node positional constraints
        self.constraints = ConstraintModel()

        self.commandsModel = None
        self.fieldEntity: FieldEntity = None

    def serialize(self) -> SerializedState:

        # generate serialized versions of the path segments and nodes
        for element in self.pathList:
            element.makeSerialized()

        # store the serialized path segments and nodes
        sList = []
        for node in self.pathList:
            sList.append(node.serialize())

        return SerializedPathState(sList, self.linker.serialize(), self.constraints.serialize())
    
    @staticmethod
    def deserialize(state: SerializedPathState) -> 'PathModel':

        model = PathModel()

        # generate deserialized versions of the path segments and nodes
        for element in state.pathList:
            element.makeDeserialized()

        # add each to linked list
        model.pathList = LinkedList[PathNodeModel | StraightSegmentEntity]()
        for element in state.pathList:
            model.pathList.addToEnd(element.deserialize())

        # deserialize other objects
        model.linker = PathCommandLinker.deserialize(state.linker)
        model.constraints = ConstraintModel.deserialize(state.constraints)
        return model

    def initCommandsModel(self, commandsModel: FullCommandsModel):
        self.commandsModel = commandsModel

    def initFieldEntity(self, fieldEntity: FieldEntity):
        self.fieldEntity = fieldEntity

    def initFirstNode(self, startPosition: tuple):

        # initialize first node
        node = self._addRawNode(startPosition) # add start node
        node.onThetaChange()

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
                
        segment = self._addRawSegment()
        node = self._addRawNode(nodePosition, isTemporary = isTemporary)

        segment.onInit()
        
        node.recomputeUI()
        segment.recomputeUI()
        self.commandsModel.ui.recomputeEntity()

        return node
    
    # insert node to split up given segment
    def insertNode(self, segment: PathSegmentModel, position: tuple, isTemporary: bool = False) -> PathNodeModel:
        previousCommand = self.linker.getCommandFromPath(segment)
        node = self._addRawNode(position, segment, previousCommand, isTemporary = isTemporary)
        
        command = self.linker.getCommandFromPath(node)
        newSegment = self._addRawSegment(node, command)

        newSegment.onInit()

        node.recomputeUI()
        newSegment.recomputeUI()
        segment.recomputeUI()
        self.commandsModel.ui.recomputeEntity()

        return node.ui
    
    # insert a node and segment at the beginning of the path
    def addNodeToBeginning(self, position: tuple, isTemporary: bool = False) -> PathNodeModel:
        node = self._addRawNodeToBeginning(position, isTemporary = isTemporary)
        
        command = self.linker.getCommandFromPath(node)
        segment = self._addRawSegment(node, command)
        
        segment.onInit()
        segment.recomputeUI()
        node.recomputeUI()

        self.commandsModel.recomputeUI()

        return node
    
    # Removing a node involves removing a node and a neighboring segment
    def deleteNode(self, node: PathNodeModel):

        # remove the node
        node.deleteUI()
        self.pathList.remove(node)

        # remvoe turn command
        turnCommand = self.linker.getCommandFromPath(node)
        turnCommand.delete()

        # remove the next segment, unless its the last segment, in which case remove the previous segment
        if node.isLastNode():
            segment = node.getPrevious()
            otherSegment = node.getNext()
        else:
            segment = node.getNext()
            otherSegment = node.getPrevious()
        
        self.pathList.remove(segment)
        segment.deleteUI()

        segmentCommand = self.linker.getCommandFromPath(segment)
        segmentCommand.delete()
        
        # the other segment is the only node/segment affected by this
        if otherSegment is not None: # it's none if there are only two nodes total and remove last one
            otherSegment.onNodePositionChange()

        # recompute the UI for commands
        self.commandsModel.recomputeUI()


    def getPathFromCommand(self, command: CommandModel) -> StraightSegmentEntity | PathNodeModel:
        return self.linker.getPathFromCommand(command)
    
    def getCommandFromPath(self, pathEntity: StraightSegmentEntity | PathNodeModel) -> CommandModel:
        return self.linker.getCommandFromPath(pathEntity)
    
    # when the segment type has changed, show the correct command and hide the others
    def onSegmentTypeChange(self, segment: StraightSegmentEntity, oldType, newType):
        segmentCommand = self.linker.getCommandFromPath(segment)
        segmentCommand.setNewAdapter(segment.getAdapter())
        segmentCommand.rebuild()
        self.commandsModel.recomputeUI()