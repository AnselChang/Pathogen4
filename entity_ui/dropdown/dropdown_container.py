from common.draw_order import DrawOrder
from common.font_manager import FontID
from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_base.text_entity import TextAlign, TextEntity
from entity_ui.group.dynamic_group_container import DynamicGroupContainer
from entity_ui.group.linear_container import LinearContainer

"""
A dropdown holds a DynamicGroupContainer that stores
each option, as well as a ImageEntity that displays
the dropdown arrow icon.
A dropdown is either expanded or collapsed. The DynamicGroupContainer
expands and collapses when the dropdown is expanded/collapsed, through
addingg/deleting LinearContainer entities. This class holds a list
of the LinearContainer options seperately.
It takes in a list of string options at initialization.
"""

class DropdownContainer(Container):

    def __init__(self, parent: Entity, options: list[str], fontID: FontID, fontSize: int, dy: int, drawOrder: DrawOrder = DrawOrder.DROPDOWN_BACKGROUND):
        super().__init__(parent, drawOrder = drawOrder)

        self.expanded = False

        

        self.recomputePosition()

        self.options: list[LinearContainer] = []
        self.group = DynamicGroupContainer(self, isHorizontal = False, entitySizePixels = dy)
        for optionStr in options:
            option = LinearContainer(self.group, optionStr, 1)
            self.options.append(option)
            TextEntity(option, fontID, fontSize, staticText = optionStr,
                       align = TextAlign.LEFT, drawOrder = DrawOrder.DROPDOWN_TEXT,
                       onClick = lambda mouse,optionStr=optionStr: self.onClick(optionStr, mouse)
            )

        self.collapse()

        self.arrow = ImageEntity(self, "dropdown_arrow", drawOrder = DrawOrder.PANEL_FOREGROUND)

    def onClick(self, optionStr: str, mouse: tuple):
        print("Clicked", optionStr)
        
    def collapse(self):
        self.expanded = False

    def expand(self):
        self.collapsed = False()