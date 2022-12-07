from enum import Enum
import pygame
from components.button import Button
from components.input import InputTextBox
from components.label import Label
from components.scene import Scene, SceneManager
from modules.game.logic import CheckResult, GameBotLogic, GameUserLogic
from utils.enum_types import MouseEvent
from utils.json_reader import JsonReader
from utils.logger import Logger
import utils.constants as constants

class GameMode(Enum):
    BOT_HOST = 0
    USER_HOST = 1

class GameBotScene(Scene):
    _instance = None

    logger = Logger(__name__).getInstance()

    CONFIG_FILE = "conf/game/GameBotScene.json"

    VALID_ANSWER_INPUT = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    
    def __init__(self) -> None:
        GameBotScene._instance = self

        self.conf = JsonReader.load(GameBotScene.CONFIG_FILE)

        self.sceneMgr = None
        self.logic: GameBotLogic = GameBotLogic.getInstance()

        self.titleLabel: Label = Label(conf=self.conf["titleLabel"])
        self.questionLabel: Label = Label(conf=self.conf["questionLabel"])
        self.messageLabel: Label = Label(conf=self.conf["messageLabel"])
        self.countLabel: Label = Label(conf=self.conf["countLabel"])
        self.answerInput: InputTextBox = InputTextBox(conf=self.conf["answerInput"])
        self.checkBtn: Button = Button(conf=self.conf["checkBtn"])

        self.init()
        
    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()

        self.checkBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onCheckClick)

    def onEnter(self) -> None:
        self.clear()

        self.logic.start()

    def input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.answerInput.popText()
                return
            if event.key not in GameBotScene.VALID_ANSWER_INPUT:
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
        GameBotScene.logger.info("GameBotScene.onCheckClick. checkResult={}".format(checkResult))
        if checkResult == CheckResult.EQUAL:
            self.sceneMgr.push(EndScene.getInstance(GameMode.BOT_HOST))
            return

        self.answerInput.clearText()
        self.messageLabel.clearText()

    def clear(self) -> None:
        self.questionLabel.clearText()
        self.messageLabel.clearText()
        self.answerInput.clearText()

    @staticmethod
    def getInstance() -> "GameBotScene":
        if GameBotScene._instance is None:
            GameBotScene()
        return GameBotScene._instance


class GameUserScene(Scene):
    _instance = None

    logger = Logger(__name__).getInstance()

    CONFIG_FILE = "conf/game/GameUserScene.json"

    VALID_ANSWER_INPUT = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    
    def __init__(self) -> None:
        GameUserScene._instance = self

        self.conf = JsonReader.load(GameUserScene.CONFIG_FILE)

        self.sceneMgr = None
        self.logic: GameUserLogic = GameUserLogic.getInstance()

        self.titleLabel: Label = Label(conf=self.conf["titleLabel"])
        self.questionLabel: Label = Label(conf=self.conf["questionLabel"])
        self.answerLabel: Label = Label(conf=self.conf["answerLabel"])
        self.lowBtn: Button = Button(conf=self.conf["lowBtn"])
        self.highBtn: Button = Button(conf=self.conf["highBtn"])
        self.correctBtn: Button = Button(conf=self.conf["correctBtn"])

        self.init()
        
    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()

        self.lowBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onLowClick)
        self.highBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onHighClick)
        self.correctBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onCorrectClick)

    def onEnter(self) -> None:
        self.clear()

        self.logic.start()

        self.logger.info("GameUserScene.onEnter. isValid={} guessNumber={}".format(self.logic.getGuessNumber(), self.logic.isValid))

        self.questionLabel.setText("Think of some number between {} and {}".format(GameUserLogic.MIN_RAND, GameUserLogic.MAX_RAND))

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)

        self.titleLabel.draw(screen)

        self.questionLabel.draw(screen)

        self.answerLabel.setText("Is {} your number?".format(self.logic.getGuessNumber()))
        self.answerLabel.draw(screen)

        self.lowBtn.draw(screen)
        self.highBtn.draw(screen)
        self.correctBtn.draw(screen)


    def onLowClick(self) -> None:
        self.logic.updateUpper()

        isValid: bool = self.logic.guess()

        if not isValid:
            self.sceneMgr.push(EndScene.getInstance(GameMode.USER_HOST))
            return

    def onHighClick(self) -> None:
        self.logic.updateLower()

        isValid: bool = self.logic.guess()

        if not isValid:
            self.sceneMgr.push(EndScene.getInstance(GameMode.USER_HOST))
            return

    def onCorrectClick(self) -> None:
        self.logic.setValid(True)
        self.sceneMgr.push(EndScene.getInstance(GameMode.USER_HOST))

    def clear(self) -> None:
        self.questionLabel.clearText()
        self.answerLabel.clearText()

    @staticmethod
    def getInstance() -> "GameUserScene":
        if GameUserScene._instance is None:
            GameUserScene()
        return GameUserScene._instance


class EndScene(Scene):
    CONFIG_FILE = "conf/game/EndScene.json"

    _instance = {}

    def __init__(self, mode: GameMode) -> None:
        EndScene._instance[mode] = self

        self.conf = JsonReader.load(EndScene.CONFIG_FILE)

        self.mode = mode
        self.logic: GameBotLogic | GameUserLogic = GameBotLogic.getInstance() if mode == GameMode.BOT_HOST else GameUserLogic.getInstance()
        self.sceneMgr = None

        self.messageLabel: Label = Label(conf=self.conf["messageLabel"])
        self.returnBtn: Button = Button(conf=self.conf["returnBtn"])

        self.init()

    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()
        self.returnBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onReturnClick)

    def onEnter(self) -> None:
        if self.mode == GameMode.BOT_HOST:
            self.messageLabel.setText("Congratulation!! You tried {} times".format(self.logic.getCount()))
        else:
            message = "Your number is {}".format(self.logic.getGuessNumber()) if self.logic.isValid else "You tricked me. I'm not playing"
            self.messageLabel.setText(message)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)

        self.messageLabel.draw(screen)
        self.returnBtn.draw(screen)

    def onReturnClick(self):
        from modules.lobby.scenes import StartScene
        self.sceneMgr.clear()
        self.sceneMgr.push(StartScene.getInstance())

    @staticmethod
    def getInstance(mode: GameMode):
        if mode not in EndScene._instance:
            EndScene(mode)
        return EndScene._instance[mode]