from common.reference_frame import PointRef, Ref
from entity_base.image.image_state import ImageStatesFactory
from entity_ui.selector_menu.configurations.common_actions import HighlightCommandAction, HighlightID
from entity_ui.selector_menu.selector_menu_factory import *
from models.path_models.path_segment_state.segment_type import SegmentType
from models.path_models.segment_direction import SegmentDirection
from entities.root_container.field_container.segment.abstract_segment_entity import AbstractSegmentEntity
from entities.root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
from models.project_history_interface import ProjectHistoryInterface

# When clicked, segment toggles forward/reverse direction
class DirectionButtonID(Enum):
    STRAIGHT_FORWARD = 0
    CURVE_FORWARD = 1
    STRAIGHT_REVERSE = 2
    CURVE_REVERSE = 3
class InvertDirectionAction(MenuClickAction[StraightSegmentEntity]):

    # Get the current direction of the segment
    def getStateID(self, targetEntity: StraightSegmentEntity) -> Enum:
        isStraight = (targetEntity.model.getType() == SegmentType.STRAIGHT)
        if targetEntity.model.getDirection() == SegmentDirection.FORWARD:
            return DirectionButtonID.STRAIGHT_FORWARD if isStraight else DirectionButtonID.CURVE_FORWARD
        else:
            return DirectionButtonID.STRAIGHT_REVERSE if isStraight else DirectionButtonID.CURVE_REVERSE

    # Toggle the forward/reverse direction
    def onClick(self, targetEntity: StraightSegmentEntity, mouse: tuple):
        targetEntity.model.toggleDirection()

        # make a save state
        ProjectHistoryInterface.getInstance().save()

# When clicked, splits segment and creates temporary node that follows mouse
class InsertNodeAction(MenuClickAction[StraightSegmentEntity]):
    def onClick(self, targetEntity: StraightSegmentEntity, mouse: tuple):

        segment = targetEntity.model

        mouseInches = segment.field.mouseToInches(mouse)
        newNode = segment.path.insertNode(segment, mouseInches, isTemporary = True)
        return newNode
    
# When clicked, splits segment and creates temporary node that follows mouse
class ToggleSegmentTypeAction(MenuClickAction[StraightSegmentEntity]):

    # Get the current segment type
    def getStateID(self, targetEntity: StraightSegmentEntity) -> Enum:
        return targetEntity.model.getType()

    def onClick(self, targetEntity: StraightSegmentEntity, mouse: tuple):
        
        current = self.getStateID(targetEntity)
        segment = targetEntity.model

        if current == SegmentType.STRAIGHT:
            segment.setState(SegmentType.ARC)
        elif current == SegmentType.ARC:
            segment.setState(SegmentType.BEZIER)
        elif current == SegmentType.BEZIER:
            segment.setState(SegmentType.STRAIGHT)
        else:
            raise Exception("Invalid segment type") 

        # make a save state
        ProjectHistoryInterface.getInstance().save()     

"""
Menu for segments. Functionality for:
    - revealing command associated with node
    - Toggle segment type
    - Toggle reverse direction
"""
def configureSegmentMenu() -> MenuDefinition:

    segmentDefinition = MenuDefinition(AbstractSegmentEntity)

    # Reveals the corresponding command
    states = ImageStatesFactory()
    states.addState(HighlightID.START_HIGHLIGHTING, ImageID.REVEAL_COMMAND, "Highlight the corresponding command")
    states.addState(HighlightID.STOP_HIGHLIGHTING, ImageID.REVEAL_COMMAND, "Stop highlighting the corresponding command")
    segmentDefinition.add(states.create(), HighlightCommandAction())
    
    # Add a button that toggles the direction of the segment
    states = ImageStatesFactory()
    states.addState(DirectionButtonID.STRAIGHT_FORWARD, ImageID.STRAIGHT_FORWARD, "Direction: forward")
    states.addState(DirectionButtonID.STRAIGHT_REVERSE, ImageID.STRAIGHT_REVERSE, "Direction: reverse")
    states.addState(DirectionButtonID.CURVE_FORWARD, ImageID.CURVE_LEFT_FORWARD, "Direction: forward")
    states.addState(DirectionButtonID.CURVE_REVERSE, ImageID.CURVE_LEFT_REVERSE, "Direction: reverse")
    segmentDefinition.add(states.create(), InvertDirectionAction())

    # Add a button that toggles segment type
    states = ImageStatesFactory()
    states.addState(SegmentType.STRAIGHT, ImageID.STRAIGHT_SEGMENT, "Segment type: straight")
    states.addState(SegmentType.ARC, ImageID.ARC_SEGMENT, "Segment type: arc")
    states.addState(SegmentType.BEZIER, ImageID.CURVE_SEGMENT, "Segment type: bezier")
    segmentDefinition.add(states.create(), ToggleSegmentTypeAction())
    
    # Inserts a node which splits this segment into two. New node is set to temporary and following mouse position
    states = ImageStatesFactory()
    states.addState(0, ImageID.ADD_NODE, "Splits this segment to insert a node")
    segmentDefinition.add(states.create(), InsertNodeAction())

    return segmentDefinition