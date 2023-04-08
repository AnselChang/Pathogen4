from entity_base.image.image_state import ImageStatesFactory
from entity_ui.selector_menu.selector_menu_factory import *
from root_container.field_container.node.path_node_entity import PathNodeEntity

"""
Menu for path nodes. Functionality for:
    - revealing command associated with node
    - add/delete intermediate turns
    - Insert node before/after
        - When clicked, special mode where wherever mouse clicks next, there will be node
        - If not beginning/end, will subdivide a segment, but new node does not have to be on segment
"""
def configureNodeMenu() -> MenuDefinition:

    segmentDefinition = MenuDefinition(PathNodeEntity)

    # Add a button that reveals the corresponding command
    states = ImageStatesFactory()
    states.addState(0, ImageID.REVERSE, "not implemented")
    segmentDefinition.add(states.create(), TestMenuClickAction(False))

    return segmentDefinition