from TextEditor.text_editor_entity import TextEditorEntity

class StaticTextEditorEntity(TextEditorEntity):

    def __init__(self, x, y,  width, height, readColor: tuple, writeColor: tuple):

        super().__init__(width, height, readColor, writeColor)

        self.x = x
        self.y = y

    # top left corner, screen ref
    def getX(self) -> float:
        return self.x
    
    # top left corner, screen ref
    def getY(self) -> float:
        return self.y
