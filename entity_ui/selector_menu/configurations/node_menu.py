from common.reference_frame import PointRef, Ref
from entity_base.entity import Entity
from entity_base.image.image_state import ImageStatesFactory
from entity_ui.selector_menu.configurations.common_actions import HighlightCommandAction, HighlightID
from entity_ui.selector_menu.selector_menu_factory import *
from root_container.field_container.node.path_node_entity import PathNodeEntity

# When clicked, start adding a node to the end of the path
class AddNodeEndAction(MenuClickAction[PathNodeEntity]):
    # entity returned is the new entity to be dragged
    def onClick(self, targetEntity: PathNodeEntity, mouse: tuple):
        newNode = targetEntity.path.addNode(PointRef(Ref.SCREEN, mouse), isTemporary = True)
        return newNode
    
# When clicked, start adding a node to the end of the path
class AddNodeBeginningAction(MenuClickAction[PathNodeEntity]):
    # entity returned is the new entity to be dragged
    def onClick(self, targetEntity: PathNodeEntity, mouse: tuple):
        newNode = targetEntity.path.addNodeToBeginning(PointRef(Ref.SCREEN, mouse), isTemporary = True)
        return newNode
    
# When clicked, deletes node on path
class DeleteNodeAction(MenuClickAction[PathNodeEntity]):

    # cannot delete if its the only node
    def isActionAvailable(self, targetEntity: PathNodeEntity | T) -> bool:
        return not (targetEntity.isFirstNode() and targetEntity.isLastNode())
    
    # entity returned is the new entity to be dragged
    def onClick(self, targetEntity: PathNodeEntity, mouse: tuple):
        targetEntity.path.removeNode(targetEntity)

class HideNodeAction(MenuClickAction[PathNodeEntity]):

    def onClick(self, targetEntity: PathNodeEntity, mouse: tuple):
        targetEntity.path.hideNode(targetEntity)
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

    # Reveals the corresponding command
    states = ImageStatesFactory()
    states.addState(HighlightID.START_HIGHLIGHTING, ImageID.REVEAL_COMMAND, "Highlight the corresponding command", None, "No turning necessary")
    states.addState(HighlightID.STOP_HIGHLIGHTING, ImageID.REVEAL_COMMAND, "Stop highlighting the corresponding command")
    segmentDefinition.add(states.create(), HighlightCommandAction())

    # Only for first node. Adds a node at the end of the path
    states = ImageStatesFactory()
    states.addState(0, ImageID.ADD_NODE, "Insert a node before the start of the path")
    segmentDefinition.add(states.create(), AddNodeBeginningAction(), lambda entity: entity.isFirstNode())

    # Only for last node. Adds a node at the end of the path
    states = ImageStatesFactory()
    states.addState(0, ImageID.ADD_NODE, "Add a node at the end of the path")
    segmentDefinition.add(states.create(), AddNodeEndAction(), lambda entity: entity.isLastNode())

    # Trash can icon. Deletes the node
    states = ImageStatesFactory()
    states.addState(0, ImageID.DELETE_NODE, "Delete this node", None, "Cannot delete the only node")
    segmentDefinition.add(states.create(), DeleteNodeAction())

    states = ImageStatesFactory()
    states.addState(0, ImageID.HIDE_NODE, "Hide this node")
    segmentDefinition.add(states.create(), HideNodeAction())

    return segmentDefinition