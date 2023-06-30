from utility.pygame_functions import getImage, brightenSurface
import pygame
from enum import Enum, auto

from utility.surface_opacity_cache import SurfaceOpacityCache


"""
Instantiates and caches all the image surface objects.
to get an image surface, do something like imageManager.get(ImageID.FIELD)
"""

class ImageID(Enum):
    FIELD = auto()
    STRAIGHT_FORWARD = auto()
    STRAIGHT_REVERSE = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    CURVE_LEFT_FORWARD = auto()
    CURVE_RIGHT_FORWARD = auto()
    CURVE_LEFT_REVERSE = auto()
    CURVE_RIGHT_REVERSE = auto()
    BEZIER = auto()
    CUSTOM = auto()
    TRASH_ON = auto()
    TRASH_OFF = auto()
    MAX_ON = auto()
    MAX_OFF = auto()
    MIN_ON = auto()
    MIN_OFF = auto()
    CHECKBOX_ON = auto()
    CHECKBOX_OFF = auto()
    ADD_NODE = auto()
    DELETE_NODE = auto()
    HIDE_NODE = auto()
    REVEAL_COMMAND = auto()
    STRAIGHT_SEGMENT = auto()
    ARC_SEGMENT = auto()
    CURVE_SEGMENT = auto()
    DROPDOWN_ICON = auto()
    WAIT = auto()
    NO_WAIT = auto()
    FOLDER_OPEN = auto()
    FOLDER_CLOSED = auto()
    VISIBLE = auto()
    INVISIBLE = auto()
    
    UNDO = auto()
    REDO = auto()

class Image:

    def __init__(self, path: str, brighten: int = 0, opacityNum = None):
        self.image = getImage("images/" + path, 1)

        if brighten != 0:
            self.image = brightenSurface(self.image, brighten)

        if opacityNum is None:
            self.cache = None
        else:
            self.cache = SurfaceOpacityCache(self.image, opacityNum)

class ImageManager:

    def get(self, id: ImageID, opacity: float = 1) -> pygame.Surface:

        if id is None:
            return None
        elif id not in self.images:
            raise Exception("ID not found:", id)

        if opacity == 1:
            return self.images[id].image
        else:
            return self.images[id].cache.get(opacity)


    def __init__(self):

        self.images: dict[ImageID, Image] = {}

        self.images[ImageID.FIELD] = Image("squarefield.png")

        self.images[ImageID.STRAIGHT_FORWARD] = Image("CommandIcons/StraightForward.png")
        self.images[ImageID.STRAIGHT_REVERSE] = Image("CommandIcons/StraightReverse.png")
        self.images[ImageID.TURN_LEFT] = Image("CommandIcons/TurnLeft.png")
        self.images[ImageID.TURN_RIGHT] = Image("CommandIcons/TurnRight.png")
        self.images[ImageID.CUSTOM] = Image("CommandIcons/Custom.png")

        self.images[ImageID.CURVE_LEFT_FORWARD] = Image("CommandIcons/CurveLeftForward.png")
        self.images[ImageID.CURVE_RIGHT_FORWARD] = Image("CommandIcons/CurveRightForward.png")
        self.images[ImageID.CURVE_LEFT_REVERSE] = Image("CommandIcons/CurveLeftReverse.png")
        self.images[ImageID.CURVE_RIGHT_REVERSE] = Image("CommandIcons/CurveRightReverse.png")

        self.images[ImageID.BEZIER] = Image("CommandIcons/Bezier.png")

        self.images[ImageID.TRASH_ON] = Image("OtherIcons/TrashOn.png")
        self.images[ImageID.TRASH_OFF] = Image("OtherIcons/TrashOff.png")

        self.images[ImageID.MAX_ON] = Image("OtherIcons/max_on.png")
        self.images[ImageID.MAX_OFF] = Image("OtherIcons/max_off.png")
        self.images[ImageID.MIN_ON] = Image("OtherIcons/min_on.png")
        self.images[ImageID.MIN_OFF] = Image("OtherIcons/min_off.png")

        brighten = 60
        self.images[ImageID.CHECKBOX_ON] = Image("widgets/checkbox_on.png", opacityNum = 20)
        self.images[ImageID.CHECKBOX_OFF] = Image("widgets/checkbox_off.png", opacityNum = 20)

        self.images[ImageID.ADD_NODE] = Image("menu/add.png")
        self.images[ImageID.DELETE_NODE] = Image("menu/delete.png")
        self.images[ImageID.REVEAL_COMMAND] = Image("menu/reveal.png")
        self.images[ImageID.HIDE_NODE] = Image("menu/hide.png")

        self.images[ImageID.STRAIGHT_SEGMENT] = Image("menu/straight_type.png")
        self.images[ImageID.ARC_SEGMENT] = Image("menu/arc_type.png")
        self.images[ImageID.CURVE_SEGMENT] = Image("menu/curve_type.png")

        self.images[ImageID.DROPDOWN_ICON] = Image("widgets/dropdown.png")

        self.images[ImageID.WAIT] = Image("OtherIcons/wait.png")
        self.images[ImageID.NO_WAIT] = Image("OtherIcons/nowait.png")

        self.images[ImageID.FOLDER_OPEN] = Image("SectionIcons/folder_open.png")
        self.images[ImageID.FOLDER_CLOSED] = Image("SectionIcons/folder_closed.png")
        self.images[ImageID.VISIBLE] = Image("SectionIcons/visible.png")
        self.images[ImageID.INVISIBLE] = Image("SectionIcons/invisible.png")

        self.images[ImageID.UNDO] = Image("TopMenuIcons/undo.png")
        self.images[ImageID.REDO] = Image("TopMenuIcons/redo.png")