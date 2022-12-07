import pygame
from components.button import Button
from components.input import InputTextBox
from components.label import Label
from components.scene import Scene, SceneManager
from modules.game.logic import CheckResult, GameLogic
from utils.event_types import MouseEvent
from utils.json_reader import JsonReader
from utils.logger import Logger
import utils.constants as constants

class StartScene(Scene):
    CONFIG_FILE = "conf/game/StartScene.json"

    _instance = None

    def __init__(self) -> None:
        StartScene._instance = self

        self.sceneMgr = None

        self.conf = JsonReader.load(StartScene.CONFIG_FILE)

        self.startBtn: Button = Button(conf=self.conf["startBtn"])

        self.init()

    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()

        self.startBtn.addEventListener(MouseEvent.ON_CLICK, self.onStartClick)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)
        self.startBtn.draw(screen)

    def onStartClick(self):
        self.sceneMgr.push(GameScene.getInstance())

    @staticmethod
    def getInstance():
        if (StartScene._instance == None):
            StartScene()
        return StartScene._instance

class GameScene(Scene):
    _instance = None

    logger = Logger(__name__).getInstance()

    CONFIG_FILE = "conf/game/GameScene.json"

    VALID_ANSWER_INPUT = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    
    def __init__(self) -> None:
        GameScene._instance = self

        self.conf = JsonReader.load(GameScene.CONFIG_FILE)

        self.sceneMgr = None
        self.logic: GameLogic = GameLogic.getInstance()

        self.titleLabel: Label = Label(conf=self.conf["titleLabel"])
        self.questionLabel: Label = Label(conf=self.conf["questionLabel"])
        self.messageLabel: Label = Label(conf=self.conf["messageLabel"])
        self.countLabel: Label = Label(conf=self.conf["countLabel"])
        self.answerInput: InputTextBox = InputTextBox(conf=self.conf["answerInput"])
        self.checkBtn: Button = Button(conf=self.conf["checkBtn"])

        self.init()
        
    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()

        self.checkBtn.addEventListener(MouseEvent.ON_CLICK, self.onCheckClick)

    def onEnter(self) -> None:
        self.clear()

        self.logic.start()

    def input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.answerInput.popText()
                return
            if event.key not in GameScene.VALID_ANSWER_INPUT:
                return

            self.answerInput.pushText(event.unicode)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)

        self.titleLabel.draw(screen)

        self.questionLabel.setText("Your number is between {} and {}".format(self.logic.getLowerHint(), self.logic.getUpperHint()))
        self.questionLabel.draw(screen)

        self.countLabel.setText("You tried {} times".format(self.logic.getCount()))
        self.countLabel.draw(screen)

        self.messageLabel.draw(screen)
        self.answerInput.draw(screen)
        self.checkBtn.draw(screen)

    def onCheckClick(self) -> None:
        answer = self.answerInput.getText()

        if answer == "": 
            self.messageLabel.setText("Please input a number")
            return

        checkResult: CheckResult = self.logic.checkAnswer(int(answer))
        GameScene.logger.info("GameScene.onCheckClick. checkResult={}".format(checkResult))
        if checkResult == CheckResult.EQUAL:
            self.sceneMgr.push(EndScene.getInstance())
            return

        self.answerInput.clearText()
        self.messageLabel.clearText()

    def clear(self) -> None:
        self.questionLabel.clearText()
        self.messageLabel.clearText()
        self.answerInput.clearText()

    @staticmethod
    def getInstance() -> "GameScene":
        if GameScene._instance is None:
            GameScene()
        return GameScene._instance

class EndScene(Scene):
    CONFIG_FILE = "conf/game/EndScene.json"

    _instance = None

    def __init__(self) -> None:
        EndScene._instance = self

        self.conf = JsonReader.load(EndScene.CONFIG_FILE)

        self.logic: GameLogic = GameLogic.getInstance()
        self.sceneMgr = None

        self.messageLabel: Label = Label(conf=self.conf["messageLabel"])
        self.returnBtn: Button = Button(conf=self.conf["returnBtn"])

        self.init()

    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()
        self.returnBtn.addEventListener(MouseEvent.ON_CLICK, self.onReturnClick)
        self.messageLabel.setText("Congratulation!! You tried {} times".format(self.logic.getCount()))

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)

        self.messageLabel.draw(screen)
        self.returnBtn.draw(screen)

    def onReturnClick(self):
        self.sceneMgr.push(StartScene.getInstance())

    @staticmethod
    def getInstance():
        if EndScene._instance is None:
            EndScene()
        return EndScene._instance