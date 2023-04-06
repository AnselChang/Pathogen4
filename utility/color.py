from utility.format_functions import hsvToRgb

class ColorTheme:

    def __init__(self, saturation, value):
        self.s = saturation
        self.v = value

    def get(self, hue) -> tuple:
        return hsvToRgb(hue, self.s, self.v)