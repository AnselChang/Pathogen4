import pygame


"""
Handles cursor and inputting text
"""

class TextHandler:

    def __init__(self, textEditor, defaultText: str | list[str] = [""]):

        self.TAB_LENGTH = 3

        self.textEditor = textEditor

        if type(defaultText) == str:
            defaultText = [defaultText]
        elif len(defaultText) == 0:
            defaultText = [""]
        self.text = defaultText.copy()

        # set cursor to the end of the text
        self.cursorY = len(self.text) - 1
        self.cursorX = len(self.text[self.cursorY])

        self.initUpper()
        

        self.textSurfaces: list[pygame.Surface] = []
        self.fullText = ""

        self.update()

    def getCursor(self) -> tuple:
        return self.cursorX, self.cursorY
 
    def currentLineLength(self):
        return len(self.text[self.cursorY])
    
    def isTabAt(self, cursorX, cursorY):

        if cursorX < self.TAB_LENGTH:
            return False

        for x in range(cursorX - self.TAB_LENGTH, cursorX):
            if self.text[cursorY][x] != " ":
                return False
        return True

    def countLeadingSpaces(self, string):
        return len(string) - len(string.lstrip())
    
    def hasPeriod(self) -> bool:
        for line in self.text:
            if "." in line:
                return True
        return False

    def onKeyDown(self, key):

        line = self.text[self.cursorY]

        # insert new line if there is room
        if key == pygame.K_RETURN:
            # can't add anymore lines
            if not self.textEditor.dynamic:
                return
            
            remainingText = line[self.cursorX:]
            self.text[self.cursorY] = self.text[self.cursorY][:self.cursorX]
            
            lastChar = line[self.cursorX - 1]
            if lastChar == ":" or lastChar == "{":
                addIndent = 1
            else:
                addIndent = 0
            
            # maintain indentation
            self.cursorY += 1
            prevLeadingSpaces = self.countLeadingSpaces(line)
            leadingSpaces = prevLeadingSpaces + addIndent * self.TAB_LENGTH
            self.text.insert(self.cursorY, " " * leadingSpaces + remainingText)
            self.cursorX = leadingSpaces
            self.textEditor.addRow()

            # add closing brace }
            if lastChar == "{":
                self.text.insert(self.cursorY + 1, " " * prevLeadingSpaces + "}")
                self.textEditor.addRow()

        # Delete the current char, or delete the line if it is empty
        elif key == pygame.K_BACKSPACE:
            if self.cursorX == 0:
                
                if self.cursorY == 0:
                    return
                remaining = self.text[self.cursorY]
                del self.text[self.cursorY]
                self.cursorY -= 1
                self.text[self.cursorY] += remaining
                self.cursorX = self.currentLineLength() - len(remaining)
                self.textEditor.removeRow()
            else:

                # delete tab
                if self.isTabAt(self.cursorX, self.cursorY):
                    self.text[self.cursorY] = line[:self.cursorX - self.TAB_LENGTH] + line[self.cursorX:]
                    self.cursorX -= self.TAB_LENGTH
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
            # for number only, can only accept decimal values
            if self.textEditor.numOnly:
                if key == pygame.K_PERIOD:
                    if self.hasPeriod():
                        return
                elif not pygame.key.name(key).isnumeric():
                    return

            # insert char at the text cursor
            if key == pygame.K_TAB:
                char = " "*self.TAB_LENGTH
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
                
            # If typed ) or ], and already exists, just move cursorX by one
            if self.cursorX < len(line):
                nextChar = line[self.cursorX]
                if (nextChar == "]" or nextChar == ")") and char == nextChar:
                    self.cursorX += 1
                    return

            inserted = line[:self.cursorX] + char + self.getMirror(char) + line[self.cursorX:]
            
            # update text list and surface
            self.text[self.cursorY] = inserted
            self.update()

            # make sure to move cursor one to the right
            self.cursorX += len(char)


        self.update()

    def update(self):
        font = self.textEditor.font.get()
        self.textSurfaces = [font.render(textLine, True, (0,0,0)) for textLine in self.text]
        self.fullText = ""
        for textLine in self.text:
            self.fullText += textLine + "\n"
        self.fullText = self.fullText[-1]

        self.maxSurfaceWidth = max(surface.get_width() for surface in self.textSurfaces)

    def getSurfaceWidth(self) -> int:
        return self.maxSurfaceWidth

    def getSurfaces(self) -> list[pygame.Surface]:
        return self.textSurfaces
    
    def getText(self) -> str:
        return self.fullText
    
    def getMirror(self, char) -> str:
        if char == "(":
            return ")"
        elif char == "[":
            return "]"
        else:
            return ""
    
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