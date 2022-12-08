import pygame

from components.label import Label

from utils.enum_types import AlignType
from utils.transform import TransformUtils

class InputTextBox:
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 40
    DEFAULT_BORDER_WIDTH = 2
    DEFAULT_PADDING = (0, 0)          # Left, top
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_TEXT_COLOR = (255, 255, 255)
    DEFAULT_TEXT_ANCHOR = AlignType.TOP_LEFT
    DEFAULT_ALIGN = AlignType.TOP_LEFT

    def __init__(self, conf: dict = None, x: int = DEFAULT_X, y: int = DEFAULT_Y, color: tuple[int, int, int] = DEFAULT_COLOR, 
            width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT, borderWidth: int = DEFAULT_BORDER_WIDTH, 
            textColor: tuple[int, int, int] = DEFAULT_TEXT_COLOR, padding: tuple[int, int] = DEFAULT_PADDING,
            textAnchor: AlignType = DEFAULT_TEXT_ANCHOR, align: AlignType = DEFAULT_ALIGN) -> None:
        self.text = ""

        if conf is not None:
            self._initWithConf(conf)
        else:
            self._initWithParams(x, y, width, height, color, width, height, borderWidth, padding, textAnchor, align)

        self.isActive = False
        self.isClicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        textPosX, textPosY = TransformUtils.alignContent(self.align, self.x + self.padding[0], self.y + self.padding[1],
            self.width - self.padding[0] * 2, self.height - self.padding[1] * 2)
        print(textPosX, textPosY, self.x, self.y, self.align)
        self.textLabel: Label = Label(color=textColor, x=textPosX, y=textPosY, anchor=self.textAnchor)

    def _initWithConf(self, conf: dict):
        self.x = conf["posX"] if "posX" in conf else InputTextBox.DEFAULT_X
        self.y = conf["posY"] if "posY" in conf else InputTextBox.DEFAULT_Y
        self.width = conf["width"] if "width" in conf else InputTextBox.DEFAULT_WIDTH
        self.height = conf["height"] if "height" in conf else InputTextBox.DEFAULT_HEIGHT
        self.color = tuple(conf["color"]) if "color" in conf else InputTextBox.DEFAULT_COLOR
        self.borderWidth = conf["borderWidth"] if "borderWidth" in conf else InputTextBox.DEFAULT_BORDER_WIDTH
        self.textColor = tuple(conf["textColor"]) if "textColor" in conf else InputTextBox.DEFAULT_TEXT_COLOR
        self.padding = tuple(conf["padding"]) if "padding" in conf else InputTextBox.DEFAULT_PADDING
        self.textAnchor = AlignType[conf["textAnchor"]] if "textAnchor" in conf else InputTextBox.DEFAULT_TEXT_ANCHOR
        self.align = AlignType[conf["align"]] if "align" in conf else InputTextBox.DEFAULT_ALIGN

    def _initWithParams(self, x: int, y: int, color: tuple[int, int, int], width: int, height: int, borderWidth: int, 
            textColor: tuple[int, int, int], padding: tuple[int, int], textAnchor: AlignType, align: AlignType):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.borderWidth = borderWidth
        self.textColor = textColor
        self.padding = padding
        self.textAnchor = textAnchor
        self.align = align

    def draw(self, screen: pygame.surface.Surface) -> None:
        pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] == 1 and not self.isClicked:
            self.isClicked = True
            self.isActive = self.rect.collidepoint(pos)
        
        if pygame.mouse.get_pressed()[0] == 0 and self.isClicked:
            self.isClicked = False

        self.textLabel.setText(self.text)
        self.textLabel.draw(screen)
        pygame.draw.rect(screen, self.color, self.rect, self.borderWidth)

    def pushText(self, text: str):
        if not self.isActive: return

        self.text += text

    def popText(self):
        if not self.isActive: return

        self.text = self.text[0:-1]

    def clearText(self):
        self.text = ""

    def getText(self):
        return self.text