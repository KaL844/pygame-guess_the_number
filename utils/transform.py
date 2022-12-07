from utils.enum_types import AlignType


class TransformUtils:
    
    @staticmethod
    def align(type: AlignType, x: int, y: int, width: int, height: int) -> tuple[int, int]:
        posX = x
        posY = y
        if type == AlignType.MID_CENTER: 
            posX = x - width // 2
            posY = y - height // 2
        elif type == AlignType.MID_RIGHT:
            posX = x - width
            posY = y - height // 2
        elif type == AlignType.MID_LEFT:
            posY = y - height // 2
        elif type == AlignType.TOP_CENTER:
            posX = x - width // 2
        elif type == AlignType.TOP_RIGHT:
            posX = x - width
        elif type == AlignType.BOTTOM_CENTER:
            posX = x - width // 2
            posY = y - height
        elif type == AlignType.BOTTOM_LEFT:
            posY = y - height
        elif type == AlignType.BOTTOM_RIGHT:
            posX = x - width
            posY = y - height
        return (posX, posY)