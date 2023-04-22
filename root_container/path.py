from command_creation.command_definition_database import CommandDefinitionDatabase
from common.draw_order import DrawOrder
from data_structures.observer import Observer
from root_container.field_container.segment.segment_type import PathSegmentType
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler
from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter
from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer

from command_creation.command_block_entity_factory import CommandBlockEntityFactory

from root_container.field_container.node.path_node_entity import PathNodeEntity
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
from root_container.field_container.field_container import FieldContainer
from root_container.panel_container.command_scrolling.command_scrolling_handler import CommandScrollingHandler

from entity_handler.entity_manager import EntityManager
from entity_handler.interactor import Interactor

from entity_base.tick_entity import TickEntity

from adapter.path_adapter import NullPathAdapter

from data_structures.linked_list import LinkedList
from common.dimensions import Dimensions
from common.reference_frame import PointRef

import entity_base.entity as entity
from root_container.path_command_linker import PathCommandLinker

"""
A class storing state for a segment and the node after it.
Also stores the relevant commands, and facilitates their interface through Adapter design pattern
"""
class Path(Observer):

    def __init__(self,
                 field: FieldContainer,
                 panel: BlockTabContentsContainer,
                 database: CommandDefinitionDatabase,
                 startPosition: PointRef):
            
        self.entities = entity._entities
        self.dimensions = entity._dimensions

        self.database = database

        self.fieldContainer = field

        self.commandHandler = panel.commandHandler
        self.commandHandler.initPath(self)
        self.pathList = LinkedList[PathNodeEntity | PathSegmentEntity]() # linked list of nodes and segments

        # store a dict that maintains a mapping from PathNodeEntity | PathSegmentEntity to CommandBlockEntity
        self.linker = PathCommandLinker()

        # initialize first node
        node = self._addRawNode(startPosition) # add start node

        node.updateAdapter()


    def _addRawNode(self, nodePosition: PointRef, afterPath = None, afterCommand = None, isTemporary: bool = False):

        if afterPath is None:
            afterPath = self.pathList.tail

        # create node and add entity
        node: PathNodeEntity = PathNodeEntity(self.fieldContainer, self, nodePosition, isTemporary)
        self.pathList.insertAfter(afterPath, node)

        turnCommand = self.commandHandler.insertCommandAfter(afterCommand, node.getAdapter())

        # maintain a relationship between the node and turn command
        self.linker.linkNode(node, turnCommand)

        return node
    
    def _addRawNodeToBeginning(self, nodePosition: PointRef, isTemporary: bool = False):

        # create node and add entity
        node: PathNodeEntity = PathNodeEntity(self.fieldContainer, self, nodePosition, isTemporary)
        self.pathList.addToBeginning(node)

        # create turn command and add entity
        turnCommand = self.commandHandler.insertCommandAtBeginning(node.getAdapter())

        # maintain a relationship between the node and turn command
        self.linker.linkNode(node, turnCommand)

        return node


    def _addRawSegment(self, afterPath = None, afterCommand = None):

        if afterPath is None:
            afterPath = self.pathList.tail

        # create segment and add entity
        segment: PathSegmentEntity = PathSegmentEntity(self.fieldContainer, self)
        self.pathList.insertAfter(afterPath, segment)

        for i, adapter in enumerate(segment.getAllAdapters()):

            segmentCommand = self.commandHandler.insertCommandAfter(afterCommand, adapter)
            self.linker.linkSegment(segment, segmentCommand)

            # Hide all but the first (straight) command
            if i != 0:
                segmentCommand.setInvisible()

            afterCommand = segmentCommand

        return segment

    # adds segment and node to the end of the path
    # return the created PathNodeEntity
    def addNode(self, nodePosition: PointRef, isTemporary: bool = False) -> PathNodeEntity:
        segment = self._addRawSegment()
        node = self._addRawNode(nodePosition, isTemporary = isTemporary)

        self.commandHandler.recomputePosition()

        node.onNodeMove()

        return node
    
    # insert node to split up given segment
    def insertNode(self, segment: PathSegmentEntity, position: PointRef, isTemporary: bool = False) -> PathNodeEntity:
        previousCommand = self.linker.getLastCommandFromSegment(segment)
        node = self._addRawNode(position, segment, previousCommand, isTemporary = isTemporary)
        
        command = self.linker.getCommandFromPath(node)
        segment = self._addRawSegment(node, command)

        self.commandHandler.recomputePosition()

        node.updateAdapter()
        node.getNext().onNodeMove(node)
        node.getPrevious().onNodeMove(node)

        return node
    
    # insert a node and segment at the beginning of the path
    def addNodeToBeginning(self, position: PointRef, isTemporary: bool = False) -> PathNodeEntity:
        node = self._addRawNodeToBeginning(position, isTemporary = isTemporary)
        
        command = self.linker.getCommandFromPath(node)
        segment = self._addRawSegment(node, command)

        self.commandHandler.recomputePosition()

        node.updateAdapter()
        node.getNext().onNodeMove(node)

        return node
    
    # Removing a node involves removing a node and a neighboring segment
    def removeNode(self, node: PathNodeEntity):

        # remove the node
        self.pathList.remove(node)
        self.entities.removeEntity(node)
        
        self.commandHandler.deleteCommand(self.linker.getCommandFromPath(node))
        self.linker.deleteNode(node)

        # remove the next segment, unless its the last segment, in which case remove the previous segment
        if node.isLastNode():
            segment = node.getPrevious()
            otherSegment = node.getNext()
        else:
            segment = node.getNext()
            otherSegment = node.getPrevious()
        
        self.pathList.remove(segment)
        self.entities.removeEntity(segment)
        
        for command in self.linker.getCommandsFromSegment(segment):
            self.commandHandler.deleteCommand(command)
        self.linker.deleteSegment(segment)

        self.commandHandler.recomputePosition()

        # the other segment is the only node/segment affected by this
        if otherSegment is not None: # it's none if there are only two nodes total and remove last one
            otherSegment.updateAdapter()
            otherSegment.recomputePosition()

        if node.getNext() is not None:
            node.getNext().getNext().onAngleChange()
        if node.getPrevious() is not None:
            node.getPrevious().getPrevious().onAngleChange()


    def getPathEntityFromCommand(self, command: CommandBlockEntity) -> PathSegmentEntity | PathNodeEntity:
        return self.linker.getPathFromCommand(command)
    
    def getCommandFromPathEntity(self, pathEntity: PathSegmentEntity | PathNodeEntity) -> CommandBlockEntity:
        return self.linker.getCommandFromPath(pathEntity)
    
    # when the segment type has changed, show the correct command and hide the others
    def onSegmentTypeChange(self, segment: PathSegmentEntity, oldType: PathSegmentType, newType: PathSegmentType):
        
        oldCommand = self.linker.getCommandFromSegmentAndType(segment, oldType)
        commandToShow = self.linker.getCommandFromSegmentAndType(segment, newType)

        for command in self.linker.getCommandsFromSegment(segment):
            if command is commandToShow:
                command.setVisible()
            else:
                command.setInvisible()

        # if old command was highlighted, then highlight the new command
        if oldCommand.isHighlighted():
            commandToShow.highlight()

        commandToShow.onFunctionChange()