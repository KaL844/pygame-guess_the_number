import random

from enum import Enum

from utils.logger import Logger

class CheckResult(Enum):
    EQUAL = "equal"
    LESS_THAN = "less"
    GREATER_THAN = "greater"
    INVALID = "invalid"

class GameLogic:
    MAX_RAND = 1000
    HINT_MIN_DISTANCE = 500
    HINT_MAX_DISTANCE = 500

    _instance = None

    logger = Logger(__name__).getInstance()
    
    def __init__(self) -> None:
        GameLogic._instance = self
        
        self.count = 0
        self.secretNumber = -1
        self.hintLowerBound = -1
        self.hintUpperBound = -1

    def start(self) -> None:
        self.count = 0
        self.secretNumber = random.randint(0, GameLogic.MAX_RAND)
        self.hintLowerBound = max(0, self.secretNumber - random.randint(GameLogic.HINT_MIN_DISTANCE, GameLogic.HINT_MAX_DISTANCE))
        self.hintUpperBound = min(GameLogic.MAX_RAND, self.secretNumber + random.randint(GameLogic.HINT_MIN_DISTANCE, GameLogic.HINT_MAX_DISTANCE))

        GameLogic.logger.info("GameLogic.start. secretNumber={} hintLowerBound={} hintUpperBound={}".format(self.secretNumber, 
            self.hintLowerBound, self.hintUpperBound))
        
    def getLowerHint(self) -> int:
        return self.hintLowerBound

    def getUpperHint(self) -> int:
        return self.hintUpperBound

    def getCount(self) -> int:
        return self.count

    def getInstance() -> "GameLogic":
        if GameLogic._instance is None:
            GameLogic()
        return GameLogic._instance

    def checkAnswer(self, answer: int) -> CheckResult:
        self.count += 1
        GameLogic.logger.info("GameLogic.checkAnswer. answer={} upperHint={} lowerHint={}".format(answer, self.hintUpperBound, self.hintLowerBound))
        if answer < self.hintLowerBound or answer > self.hintUpperBound:
            return CheckResult.INVALID
        elif answer < self.secretNumber: 
            self.hintLowerBound = answer
            return CheckResult.GREATER_THAN
        elif answer > self.secretNumber: 
            self.hintUpperBound = answer
            return CheckResult.LESS_THAN
        return CheckResult.EQUAL