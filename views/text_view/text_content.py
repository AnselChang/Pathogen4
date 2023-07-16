from data_structures.observer import Observable
from views.text_view.text_view_config import Submit, TextConfig
import re

"""
Handles the text content logic itself, such as
adding and removing text, text validation,
maximum text length, etc.

Note that this isn't necessarily synced with the variable.
While editing, the variable isn't updated until the content
is submit-valid and the user leaves the text editor.
"""
class TextContent(Observable): # send a notif when content is updated

    def __init__(self, config: TextConfig, startingText: str):

        super().__init__()

        self.config = config

        self.reDisplay = re.compile(config.validDisplay)
        self.reSubmit = re.compile(config.validSubmit)

        self.submitValid: Submit = Submit.VALID

        self.content: list[str] = None
        self.cursorX: int = None
        self.cursorY: int = None
        self.setContentFromString(startingText)

    # given a string possibly delimited by newlines, convert to a list of strings
    # and set the content to that
    # if not valid, throw an error
    def setContentFromString(self, string: str):

        self.content: list[str] = []

        lines = string.split("\n")
        for line in lines:
            if not (self.reDisplay.fullmatch(line) and self.reSubmit.fullmatch(line))
                raise Exception("Invalid string")
            self.content.append(line)

        # update cursor to be at end of text
        self.cursorY = len(self.content) - 1
        self.cursorX = len(self.content[self.cursorY])

    # return the content as a single string delimited by newlines
    # no newlines at beginning or end
    def getContentAsString(self) -> str:
        return "\n".join(self.content)
    
    def getContentAsList(self) -> list[str]:
        return self.content
    
    # get the number of lines in the content
    def getCharHeight(self) -> int:
        return len(self.content)
    
    # get the char length of the longest line in the content
    def getMaxCharWidth(self) -> int:
        return max([len(line) for line in self.content])
    
    def getCursorPosition(self) -> tuple:
        return self.cursorX, self.cursorY
    
    # update cache of whether the content is valid to submit
    def _updateSubmitValid(self):
        self.submitValid = Submit.VALID
        for line in self.content:
            if not self.reSubmit.fullmatch(line):
                self.submitValid = Submit.INVALID
                break
    
    # Whether the content is valid to submit
    def isSubmitValid(self) -> Submit:
        return self.submitValid
    
    # possibly update content based on keypress, which
    # could be a character, backspace, enter key, arrows, etc.
    # return whether the content was updated
    def handleKeyPress(self, key) -> bool:
        pass

        self._updateSubmitValid()
        self.notify()