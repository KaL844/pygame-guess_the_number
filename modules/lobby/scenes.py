import pygame
from components.button import Button
from components.scene import Scene, SceneManager
from modules.game.scenes import GameBotScene, GameUserScene
from utils.enum_types import MouseEvent
from utils.json_reader import JsonReader
import utils.constants as constants


class StartScene(Scene):
    CONFIG_FILE = "conf/lobby/StartScene.json"

    _instance = None

    def __init__(self) -> None:
        StartScene._instance = self

        self.sceneMgr = None

        self.conf = JsonReader.load(StartScene.CONFIG_FILE)

        self.startBotHostBtn: Button = Button(conf=self.conf["startBotHostBtn"])
        self.startUserHostBtn: Button = Button(conf=self.conf["startUserHostBtn"])

        self.init()

    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()

        self.startBotHostBtn.addEventListener(MouseEvent.ON_CLICK, self.onStartBotHostClick)
        self.startUserHostBtn.addEventListener(MouseEvent.ON_CLICK, self.onStartUserHostClick)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)
        self.startBotHostBtn.draw(screen)
        self.startUserHostBtn.draw(screen)

    def onStartBotHostClick(self):
        self.sceneMgr.push(GameBotScene.getInstance())

    def onStartUserHostClick(self):
        self.sceneMgr.push(GameUserScene.getInstance())

    @staticmethod
    def getInstance():
        if (StartScene._instance == None):
            StartScene()
        return StartScene._instance