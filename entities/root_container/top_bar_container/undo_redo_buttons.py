from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from models.project_history_model import ProjectHistoryModel
from entities.root_container.top_bar_container.top_bar_button_container import ButtonClickAction, ButtonDefinition

class UndoButtonAction(ButtonClickAction):

    def isActionAvailable(self) -> bool:
        return ProjectHistoryModel.getInstance().canUndo()

    def onClick(self):
        ProjectHistoryModel.getInstance().undo()

class UndoButtonDefinition(ButtonDefinition):

    def __init__(self):
        state = ImageState(0, ImageID.UNDO, "Undo")
        super().__init__(state, UndoButtonAction())

class RedoButtonAction(ButtonClickAction):
    
    def isActionAvailable(self) -> bool:
        return ProjectHistoryModel.getInstance().canRedo()

    def onClick(self):
        ProjectHistoryModel.getInstance().redo()

class RedoButtonDefinition(ButtonDefinition):
     
    def __init__(self):
        state = ImageState(0, ImageID.REDO, "Redo")
        super().__init__(state, RedoButtonAction())