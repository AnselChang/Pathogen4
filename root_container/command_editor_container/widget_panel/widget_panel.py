from entity_base.panel_container import PanelContainer

"""
Widget panel is on the top left side of command editor.
Shows the widgets and readouts to be dragged to command.
"""

class WidgetPanel(PanelContainer):
    
     def __init__(self, parent,
        px: float,
        py: float,
        pw: float,
        ph: float,
        padding: float,
        color: tuple = None,
        radius: float = 0
    ):
        
        super().__init__(parent, px, py, pw, ph, padding, color, radius)