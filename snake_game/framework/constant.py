from enum import Enum
from .utils import Point


# Color Constant
BLK_COLOR = "white"
DEF_COLOR = "black"


# Direction Constant
DIR_UP = Point(0, -1)
DIR_DOWN = Point(0, 1)
DIR_LEFT = Point(-1, 0)
DIR_RIGHT = Point(1, 0)


# Align Constant
class EnumAlign(Enum):
    TOPLEFT = 0
    TOPCENTER = 1
    TOPRIGHT = 2

    MIDDLELEFT = 3
    MIDDLECENTER = 4
    MIDDLERIGHT = 5

    BOTLEFT = 6
    BOTCENTER = 7
    BOTRIGHT = 8
