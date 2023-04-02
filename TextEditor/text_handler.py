from pygame_functions import drawText, FONTCODE
import pygame


"""
Handles cursor and inputting text
"""

class TextHandler:

    def __init__(self, textEditor, defaultText: str | list[str] = [""]):

        self.textEditor = textEditor

        if type(defaultText) == str:
            defaultText = [defaultText]
        elif len(defaultText) == 0:
            defaultText = [""]
        self.text = defaultText

        # set cursor to the end of the text
        self.cursorY = len(self.text) - 1
        self.cursorX = len(self.text[self.cursorY])

        self.initUpper()
        

        self.textSurfaces: list[pygame.Surface] = []
        self.fullText = ""

        self.update()

    def getCursor(self) -> tuple:
        return self.cursorX, self.cursorY

    def isTextTooLong(self, text):
        width = FONTCODE.render(text, True, (0,0,0)).get_width()
        return width > self.textEditor.getMaxTextWidth()
    
    def currentLineLength(self):
        return len(self.text[self.cursorY])

    def onKeyDown(self, key):

        line = self.text[self.cursorY]

        # insert new line if there is room
        if key == pygame.K_RETURN:
            # can't add anymore lines
            if len(self.text) == self.textEditor.getMaxTextLines() and not self.textEditor.extendLine():
                return
            self.cursorY += 1
            self.text.insert(self.cursorY, "")
            self.cursorX = 0

        # Delete the current char, or delete the line if it is empty
        elif key == pygame.K_BACKSPACE:
            if self.cursorX == 0:
                
                if self.cursorY == 0:
                    return
                
                del self.text[self.cursorY]
                self.cursorY -= 1
                self.cursorX = self.currentLineLength()
            else:
                self.text[self.cursorY] = line[:self.cursorX - 1] + line[self.cursorX:]
                self.cursorX -= 1
        elif key == pygame.K_LEFT:
            if self.cursorX > 0:
                self.cursorX -= 1
            elif self.cursorY > 0:
                self.cursorY -= 1
                self.cursorX = self.currentLineLength()
        elif key == pygame.K_RIGHT:
            if self.cursorX < self.currentLineLength():
                self.cursorX += 1
            elif self.cursorY < len(self.text) - 1:
                self.cursorY += 1
                self.cursorX = 0
        elif key == pygame.K_UP:
            if self.cursorY > 0:
                self.cursorY -= 1
                self.cursorX = min(self.cursorX, self.currentLineLength())
        elif key == pygame.K_DOWN:
            if self.cursorY < len(self.text) - 1:
                self.cursorY += 1
                self.cursorX = min(self.cursorX, self.currentLineLength())
        else:
            # insert char at the text cursor
            if key == pygame.K_TAB:
                char = "   "
            elif key == pygame.K_SPACE:
                char = " "
            else:
                char = pygame.key.name(key)
                if len(char) != 1:
                    return
                
            # to upper case
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                char = self.getUpper(char)
                if char is None:
                    return

            inserted = line[:self.cursorX] + char + line[self.cursorX:]

            # abort if exceeds max text width
            if self.isTextTooLong(inserted):
                return
            
            # update text list and surface
            self.text[self.cursorY] = inserted
            self.update()

            # make sure to move cursor one to the right
            self.cursorX += len(char)


        self.update()

    def update(self):
        self.textSurfaces = [FONTCODE.render(textLine, True, (0,0,0)) for textLine in self.text]
        self.fullText = ""
        for textLine in self.text:
            self.fullText += textLine + "\n"
        self.fullText = self.fullText[-1]

    def getSurfaces(self) -> list[pygame.Surface]:
        return self.textSurfaces
    
    def getText(self) -> str:
        return self.fullText
    
    def getUpper(self, char) -> str:
        if char.isalpha():
            return char.upper()
        elif char in self.shifted_chars:
            return self.shifted_chars[char]
        else:
            return None

    def initUpper(self):
        self.shifted_chars = {
            "1": "!",
            "2": "@",
            "3": "#",
            "4": "$",
            "5": "%",
            "6": "^",
            "7": "&",
            "8": "*",
            "9": "(",
            "0": ")",
            "-": "_",
            "=": "+",
            "[": "{",
            "]": "}",
            "\\": "|",
            ";": ":",
            "'": "\"",
            ",": "<",
            ".": ">"
        }