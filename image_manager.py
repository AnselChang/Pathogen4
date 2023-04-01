from pygame_functions import getImage
import pygame
from enum import Enum, auto

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
    CUSTOM = auto()
    TRASH_ON = auto()
    TRASH_OFF = auto()
    MAX_ON = auto()
    MAX_OFF = auto()
    MIN_ON = auto()
    MIN_OFF = auto()

class Image:

    def __init__(self, path: str, imageScale: float = 1):
        self.image = getImage("Images/" + path, imageScale)

class ImageManager:

    def get(self, id: ImageID) -> Image:
        return self.images[id].image

    def __init__(self):

        self.images: dict[ImageID, Image] = {}

        self.images[ImageID.FIELD] = Image("squarefield.png")

        size = 0.045
        self.images[ImageID.STRAIGHT_FORWARD] = Image("CommandIcons/StraightForward.png", size)
        self.images[ImageID.STRAIGHT_REVERSE] = Image("CommandIcons/StraightReverse.png", size)
        self.images[ImageID.TURN_LEFT] = Image("CommandIcons/TurnLeft.png", size)
        self.images[ImageID.TURN_RIGHT] = Image("CommandIcons/TurnRight.png", size)
        self.images[ImageID.CUSTOM] = Image("CommandIcons/Custom.png", size)

        size = 0.03
        self.images[ImageID.TRASH_ON] = Image("OtherIcons/TrashOn.png", size)
        self.images[ImageID.TRASH_OFF] = Image("OtherIcons/TrashOff.png", size)

        size = 0.07
        self.images[ImageID.MAX_ON] = Image("OtherIcons/max_on.png", size)
        self.images[ImageID.MAX_OFF] = Image("OtherIcons/max_off.png", size)
        self.images[ImageID.MIN_ON] = Image("OtherIcons/min_on.png", size)
        self.images[ImageID.MIN_OFF] = Image("OtherIcons/min_off.png", size)