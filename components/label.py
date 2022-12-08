import pygame

from utils.enum_types import AlignType
from utils.transform import TransformUtils

pygame.init()

class Label:
    DEFAULT_TEXT = ""
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_FONT = pygame.font.Font(None, 30)
    DEFAULT_SMOOTH = True
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_ANCHOR = AlignType.TOP_LEFT

    def __init__(self, conf: dict = None, text: str = DEFAULT_TEXT, color: tuple[int, int, int] = DEFAULT_COLOR, 
            font: pygame.font.Font = DEFAULT_FONT, x: int = DEFAULT_X, y: int = DEFAULT_Y, isSmooth: bool = DEFAULT_SMOOTH, 
            anchor: AlignType = DEFAULT_ANCHOR) -> None:

        if conf is not None:
            self._initWithConf(conf)
        else:
            self._initWithParams(text, color, x, y, isSmooth, anchor)
        
        self.font = font

    def _initWithConf(self, conf: dict) -> None:
        self.text = conf["text"] if "text" in conf else Label.DEFAULT_TEXT
        self.color = tuple(conf["color"]) if "color" in conf else Label.DEFAULT_COLOR
        self.x = conf["posX"] if "posX" in conf else Label.DEFAULT_X
        self.y = conf["posY"] if "posY" in conf else Label.DEFAULT_Y
        self.isSmooth = conf["isSmooth"] if "isSmooth" in conf else Label.DEFAULT_SMOOTH
        self.anchor = AlignType[conf["anchor"]] if "anchor" in conf else Label.DEFAULT_ANCHOR

    def _initWithParams(self, text: str, color: tuple[int, int, int], x: int, y: int, isSmooth: bool, anchor: AlignType) -> None:
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.isSmooth = isSmooth
        self.anchor = anchor

    def draw(self, screen: pygame.surface.Surface) -> None:
        textImg = self.font.render(self.text, self.isSmooth, self.color)
        posX, posY = TransformUtils.alignAnchor(self.anchor, self.x, self.y, textImg.get_size()[0], textImg.get_size()[1])
        screen.blit(textImg, (posX, posY))

    def setText(self, text: str) -> None:
        self.text = text

    def clearText(self) -> None:
        self.text = ""