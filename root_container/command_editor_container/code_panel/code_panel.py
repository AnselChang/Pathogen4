from entity_base.panel_container import PanelContainer

"""
Code panel is on the bottom left side of the command editor.
Code editor box.
"""

class CodePanel(PanelContainer):
    
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

