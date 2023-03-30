from pygame_functions import getImage
import pygame
from enum import Enum, auto

class ImageID(Enum):
    STRAIGHT_FORWARD = auto()
    STRAIGHT_REVERSE = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    CUSTOM = auto()
    TRASH_ON = auto()
    TRASH_OFF = auto()

class Image:

    def __init__(self, path: str, imageScale: float):
        self.image = getImage("Images/" + path, imageScale)

class ImageManager:

    def get(self, id: ImageID) -> Image:
        return self.images[id].image

    def __init__(self):

        self.images: dict[ImageID, Image] = {}

        size = 0.045
        self.images[ImageID.STRAIGHT_FORWARD] = Image("CommandIcons/StraightForward.png", size)
        self.images[ImageID.STRAIGHT_REVERSE] = Image("CommandIcons/StraightReverse.png", size)
        self.images[ImageID.TURN_LEFT] = Image("CommandIcons/TurnLeft.png", size)
        self.images[ImageID.TURN_RIGHT] = Image("CommandIcons/TurnRight.png", size)
        self.images[ImageID.CUSTOM] = Image("CommandIcons/Custom.png", size)

        size = 0.03
        self.images[ImageID.TRASH_ON] = Image("OtherIcons/TrashOn.png", size)
        self.images[ImageID.TRASH_OFF] = Image("OtherIcons/TrashOff.png", size)