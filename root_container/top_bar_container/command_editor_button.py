from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from models.ui_model import CommandEditorStatus, UIModel
from root_container.top_bar_container.top_bar_button_container import ButtonClickAction, ButtonDefinition

"""
The button that toggles displaying the command editor
"""

# Clicking button should toggle command editor status
# always available to click
class CommandEditorButtonAction(ButtonClickAction):

    def __init__(self):
        super().__init__()
        self.uiModel = UIModel.getInstance()
    
    # Poll from model whether command editor is shown
    def getStateID(self) -> CommandEditorStatus:
        return self.uiModel.getCommandEditorStatus()

    # toggle command editor visibility
    def onClick(self):
        if self.uiModel.getCommandEditorStatus() == CommandEditorStatus.HIDDEN:
            self.uiModel.showCommandEditor()
        else:
            self.uiModel.hideCommandEditor()

class CommandEditorButtonDefinition(ButtonDefinition):

    def __init__(self):

        # state when not showing command editor
        normalState = ImageState(CommandEditorStatus.HIDDEN, ImageID.CHECKBOX_OFF, "Show command editor")

        # state when showing command editor
        editorState = ImageState(CommandEditorStatus.SHOWN, ImageID.CHECKBOX_ON, "Go back to path")

        super().__init__([normalState, editorState], CommandEditorButtonAction())