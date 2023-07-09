from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from entity_base.notifying_variable import NotifyingVariable
from models.ui_model import CommandEditorStatus, UIModel
from entities.root_container.top_bar_container.top_bar_button_container import ButtonClickAction, ButtonDefinition
import multiprocessing as mp

"""
The button that toggles displaying the command editor
"""

# Clicking button should toggle command editor status
# always available to click
class CommandEditorButtonAction(ButtonClickAction):

    def __init__(self, runCommandsWindowFunction):
        super().__init__()
        self.uiModel = UIModel.getInstance()
        self.runCommandsWindow = runCommandsWindowFunction
    
    # Poll from model whether command editor is shown
    def getStateID(self) -> CommandEditorStatus:
        return self.uiModel.getCommandEditorStatus()

    def openCommandEditorWindow(self):
        # create commands process and window
        isProcessDone = mp.Value('i', 0)

        # run callback when commands process is done
        NotifyingVariable(lambda: isProcessDone.value, lambda value: UIModel.getInstance().hideCommandEditor())

        #mp.set_start_method('spawn')
        commandsProcess = mp.Process(target = self.runCommandsWindow, args=(isProcessDone,))
        commandsProcess.start()

    # toggle command editor visibility
    def onClick(self):
        if self.uiModel.getCommandEditorStatus() == CommandEditorStatus.HIDDEN:
            self.openCommandEditorWindow()
            self.uiModel.showCommandEditor()


class CommandEditorButtonDefinition(ButtonDefinition):

    def __init__(self, runCommandsWindowFunction):

        # state when not showing command editor
        normalState = ImageState(CommandEditorStatus.HIDDEN, ImageID.CHECKBOX_OFF, "Show command editor")

        # state when showing command editor
        editorState = ImageState(CommandEditorStatus.SHOWN, ImageID.CHECKBOX_ON, "Go back to path")

        super().__init__([normalState, editorState], CommandEditorButtonAction(runCommandsWindowFunction))