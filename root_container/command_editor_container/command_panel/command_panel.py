from entity_base.panel_container import PanelContainer

"""
Command panel is on the right side of command editor.
Shows the commands and the command being edited
"""

class CommandPanel(PanelContainer):
    
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