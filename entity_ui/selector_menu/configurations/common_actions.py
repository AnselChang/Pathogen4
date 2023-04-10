from entity_ui.selector_menu.selector_menu_factory import MenuClickAction
from root_container.field_container.node.path_node_entity import PathNodeEntity
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity

# When clicked, highlight command and move scrollbar to make it visible
class HighlightCommandAction(MenuClickAction[PathNodeEntity | PathSegmentEntity]):

    def isActionAvailable(self, targetEntity: PathNodeEntity | PathSegmentEntity) -> bool:
        if isinstance(targetEntity, PathNodeEntity) and not targetEntity.isTurnEnabled():
            return False
        return True

    # entity returned is the new entity to be dragged
    def onClick(self, targetEntity: PathNodeEntity | PathSegmentEntity, mouse: tuple):
        command = targetEntity.path.dict[targetEntity]
        command.highlight()
