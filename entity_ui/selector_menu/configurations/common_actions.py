from enum import Enum
from entity_ui.selector_menu.selector_menu_factory import MenuClickAction
from root_container.field_container.node.path_node_entity import PathNodeEntity
from root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity

class HighlightID(Enum):
    START_HIGHLIGHTING = 1
    STOP_HIGHLIGHTING = 2

# When clicked, highlight command and move scrollbar to make it visible
class HighlightCommandAction(MenuClickAction[PathNodeEntity | StraightSegmentEntity]):

    # If already highlighted, tooltip indicates that clicking should dehighlight
    def getStateID(self, targetEntity: StraightSegmentEntity) -> Enum:
        if not self.isActionAvailable(targetEntity):
            return HighlightID.START_HIGHLIGHTING
        
        command = targetEntity.path.getCommandFromPathEntity(targetEntity)
        if command.isHighlighted():
            return HighlightID.STOP_HIGHLIGHTING
        else:
            return HighlightID.START_HIGHLIGHTING

    def isActionAvailable(self, targetEntity: PathNodeEntity | StraightSegmentEntity) -> bool:
        if isinstance(targetEntity, PathNodeEntity) and not targetEntity.isTurnEnabled():
            return False
        return True

    # entity returned is the new entity to be dragged
    def onClick(self, targetEntity: PathNodeEntity | StraightSegmentEntity, mouse: tuple):
        command = targetEntity.path.getCommandFromPathEntity(targetEntity)
        command.highlightUI()
