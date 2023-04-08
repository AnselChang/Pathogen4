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

    return segmentDefinition