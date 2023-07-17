from data_structures.observer import Observable
from views.text_view.text_utility import SHIFT_CHARS
from views.text_view.text_view_config import TextConfig
import re, pygame

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

        self.submitValid: bool = True

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
    
    # return the content as a list of strings, replacing tabs with 4 spaces
    def getDisplayableContent(self) -> list[str]:
        return [line.replace("\t", " " * 4) for line in self.content]
    
    # get the number of lines in the content
    def getCharHeight(self) -> int:
        return len(self.content)
    
    def getCharWidthAtLine(self, lineNumber: int) -> int:
        line = self.content[lineNumber]
        line = line.replace("\t", " " * 4) # replace tabs with 4 spaces
        return len(line)
    
    # get the char length of the longest line in the content
    def getMaxCharWidth(self) -> int:
        return max([len(line) for line in self.content])
    
    def getCursorPosition(self) -> tuple:
        return self.cursorX, self.cursorY
    
    # update cache of whether the content is valid to submit
    def _updateSubmitValid(self):
        self.submitValid = True
        for line in self.content:
            if self.reSubmit.fullmatch(line) is None:
                self.submitValid = False
                break
    
    # Whether the content is valid to submit
    # calculations are cached so this is O(1)
    def isSubmitValid(self) -> bool:
        return self.submitValid
    
    # Whether the content is valid to display
    # do not need to cache as this is called once right after content is updated
    def isDisplayValid(self) -> bool:
        for line in self.content:
            if self.reDisplay.fullmatch(line) is None:
                return False
        return True
    
    # given a hypothetical content, return whether it is within the bounds
    # and whether it is valid to display
    def isContentLegal(self) -> bool:

        # If horizontal bounds are static and exceeded, content is out of bounds
        if not self.config.expandWidth:
            if self.getMaxCharWidth() > self.config.charWidth:
                return False
        
        # If vertical bounds are static and exceeded, content is out of bounds
        if not self.config.expandHeight:
            if self.getCharHeight() > self.config.charHeight:
                return False
            
        return self.isDisplayValid()


    
    # possibly update content based on keypress, which
    # could be a character, backspace, enter key, arrows, etc.
    # return whether the content was updated
    def onKeystroke(self, key) -> bool:

        # cache old content to revert if modifications make content illegal
        oldContent = self.content.copy()
        
        # update content
        self._handleKeystroke(key)

        if not self.isContentLegal():
            # if content is illegal, revert
            self.content = oldContent
            return False
        else:
            # Otherwise, update submitValid and notify observers of content change
            self._updateSubmitValid()
            self.notify()
            return True
        
    def _getMirror(self, char) -> str:
        if char == "(":
            return ")"
        elif char == "[":
            return "]"
        else:
            return ""
        
    def _handleKeystroke(self, key: pygame.Key) -> list[str]:

        # insert new line if there is room
        if key == pygame.K_RETURN:
            pass
        # Delete the current char, or delete the line if it is empty
        elif key == pygame.K_BACKSPACE:
            pass
        elif key == pygame.K_LEFT:
            if self.cursorX > 0:
                self.cursorX -= 1
            elif self.cursorY > 0:
                self.cursorY -= 1
                self.cursorX = self.getCharWidthAtLine(self.cursorY)
        elif key == pygame.K_RIGHT:
            if self.cursorX < self.getCharWidthAtLine(self.cursorY):
                self.cursorX += 1
            elif self.cursorY < self.getCharHeight() - 1:
                self.cursorY += 1
                self.cursorX = 0
        elif key == pygame.K_UP:
            if self.cursorY > 0:
                self.cursorY -= 1
                self.cursorX = min(self.cursorX, self.getCharWidthAtLine(self.cursorY))
        elif key == pygame.K_DOWN:
            if self.cursorY < self.getCharHeight() - 1:
                self.cursorY += 1
                self.cursorX = min(self.cursorX, self.getCharWidthAtLine(self.cursorY))
        else:

            # if the key is a character, insert it into the content
            name = pygame.key.name(key)
            
            allKeys = pygame.key.get_pressed()
            isShift = allKeys[pygame.K_LSHIFT] or allKeys[pygame.K_RSHIFT]

            # convert into a single-character string to be inserted
            if key == pygame.K_TAB:
                char = "\t"
            elif len(name) == 1:
                if isShift and name in SHIFT_CHARS: # convert special character to shifted
                    char = SHIFT_CHARS[name]
                elif isShift and name.isalpha(): # convert letter to uppercase
                    char = name.upper()
                else:
                    char = name # leave as is for normal characters
            else:
                char = None

            # if the key is a character, insert it into the content
            if char is not None:
                before = self.content[:self.cursorX]
                after = self.content[self.cursorX:]
                self.content[self.cursorY] = before + char + self._getMirror(char) + after