from entity_base.text_entity import TextEntity, TextAlign

"""
A subclass of TextEntity. Inside a RowEntity, the label is always on the left column
"""

class LabelEntity(TextEntity):

    def __init__(self, parent, font, size, staticText: str = None):
        super().__init__(parent, font, size, staticText + ":", align = TextAlign.RIGHT)

    def defineRightX(self) -> tuple:
        return self._px(0.65)
    
    def defineCenterY(self) -> float:
        return self._py(0.46)

    # widgets and readouts should not use ElementEntity width
    # because they are dynamic
    def defineWidth(self) -> float:
        return self._pwidth(0)
    
    def defineHeight(self) -> float:
        return self._pheight(1)