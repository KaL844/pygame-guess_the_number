import pygame

from components.label import Label

class InputTextBox:
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 40
    DEFAULT_BORDER_WIDTH = 2
    DEFAULT_PADDING = (0, 0, 0, 0)          # Left, right, top, bottom
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_TEXT_COLOR = (255, 255, 255)

    def __init__(self, conf: dict = None, x: int = DEFAULT_X, y: int = DEFAULT_Y, color: tuple[int, int, int] = DEFAULT_COLOR, 
            width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT, borderWidth: int = DEFAULT_BORDER_WIDTH, 
            textColor: tuple[int, int, int] = DEFAULT_TEXT_COLOR, padding: tuple[int, int, int, int] = DEFAULT_PADDING) -> None:
        self.text = ""

        if conf is not None:
            self._initWithConf(conf)
        else:
            self._initWithParams(x, y, width, height, color, width, height, borderWidth, padding)

        self.isActive = False
        self.isClicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textLabel: Label = Label(color=textColor, x=(self.x + self.padding[0]), y=(self.y + self.padding[2]))

    def _initWithConf(self, conf: dict):
        self.x = conf["posX"] if "posX" in conf else InputTextBox.DEFAULT_X
        self.y = conf["posY"] if "posY" in conf else InputTextBox.DEFAULT_Y
        self.width = conf["width"] if "width" in conf else InputTextBox.DEFAULT_WIDTH
        self.height = conf["height"] if "height" in conf else InputTextBox.DEFAULT_HEIGHT
        self.color = tuple(conf["color"]) if "color" in conf else InputTextBox.DEFAULT_COLOR
        self.borderWidth = conf["borderWidth"] if "borderWidth" in conf else InputTextBox.DEFAULT_BORDER_WIDTH
        self.textColor = tuple(conf["textColor"]) if "textColor" in conf else InputTextBox.DEFAULT_TEXT_COLOR
        self.padding = tuple(conf["padding"]) if "padding" in conf else InputTextBox.DEFAULT_PADDING

    def _initWithParams(self, x: int, y: int, color: tuple[int, int, int], width: int, height: int, borderWidth: int, 
            textColor: tuple[int, int, int], padding: tuple[int, int, int, int]):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.borderWidth = borderWidth
        self.textColor = textColor
        self.padding = padding

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