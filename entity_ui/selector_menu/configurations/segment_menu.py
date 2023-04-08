from common.reference_frame import PointRef, Ref
from entity_base.image.image_state import ImageStatesFactory
from entity_ui.selector_menu.selector_menu_factory import *
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity, SegmentDirection

# When clicked, segment toggles forward/reverse direction
class InvertDirectionAction(MenuClickAction[PathSegmentEntity]):

    # Get the current direction of the segment
    def getStateID(self, targetEntity: PathSegmentEntity) -> Enum:
        return targetEntity.getDirection()

    # Toggle the forward/reverse direction
    def onClick(self, targetEntity: PathSegmentEntity, mouse: tuple):
        targetEntity.toggleDirection()

# When clicked, splits segment and creates temporary node that follows mouse
class InsertNodeAction(MenuClickAction[PathSegmentEntity]):
    def onClick(self, targetEntity: PathSegmentEntity, mouse: tuple):
        newNode = targetEntity.path.insertNode(targetEntity, PointRef(Ref.SCREEN, mouse), isTemporary = True)
        return newNode

"""
Menu for segments. Functionality for:
    - revealing command associated with node
    - Toggle segment type
    - Toggle reverse direction
"""
def configureSegmentMenu() -> MenuDefinition:

    segmentDefinition = MenuDefinition(PathSegmentEntity)

    # Add a button that reveals the corresponding command
    states = ImageStatesFactory()
    states.addState(0, ImageID.CHECKBOX_ON, "not implemented")
    segmentDefinition.add(states.create(), TestMenuClickAction(False))
    
    # Add a button that toggles the direction of the segment
    states = ImageStatesFactory()
    states.addState(SegmentDirection.FORWARD, ImageID.STRAIGHT_FORWARD, "Direction: forward")
    states.addState(SegmentDirection.REVERSE, ImageID.STRAIGHT_REVERSE, "Direction: reverse")
    segmentDefinition.add(states.create(), InvertDirectionAction())

    # Inserts a node which splits this segment into two. New node is set to temporary and following mouse position
    states = ImageStatesFactory()
    states.addState(0, ImageID.ADD_NODE, "Splits this segment to insert a node")
    segmentDefinition.add(states.create(), InsertNodeAction())

    return segmentDefinition