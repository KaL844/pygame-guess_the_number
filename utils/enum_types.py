from enum import Enum


class MouseEvent(Enum):
    ON_CLICK = 1

class AlignType(Enum):
    MID_CENTER = 0
    MID_RIGHT = 1
    MID_LEFT = 2
    TOP_CENTER = 3
    TOP_RIGHT = 4
    TOP_LEFT = 5
    BOTTOM_CENTER = 6
    BOTTOM_RIGHT = 7
    BOTTOM_LEFT = 8
    