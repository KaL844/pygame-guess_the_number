import random

from enum import Enum

from utils.logger import Logger

class CheckResult(Enum):
    EQUAL = "equal"
    LESS_THAN = "less"
    GREATER_THAN = "greater"
    INVALID = "invalid"

class GameBotLogic:
    MAX_RAND = 1000
    MIN_RAND = 0
    HINT_MIN_DISTANCE = 500
    HINT_MAX_DISTANCE = 500

    _instance = None

    logger = Logger(__name__).getInstance()
    
    def __init__(self) -> None:
        GameBotLogic._instance = self
        
        self.count = 0
        self.secretNumber = -1
        self.hintLowerBound = -1
        self.hintUpperBound = -1

    def start(self) -> None:
        self.count = 0
        self.secretNumber = random.randint(GameBotLogic.MIN_RAND, GameBotLogic.MAX_RAND)
        self.hintLowerBound = max(GameBotLogic.MIN_RAND, self.secretNumber - random.randint(GameBotLogic.HINT_MIN_DISTANCE, GameBotLogic.HINT_MAX_DISTANCE))
        self.hintUpperBound = min(GameBotLogic.MAX_RAND, self.secretNumber + random.randint(GameBotLogic.HINT_MIN_DISTANCE, GameBotLogic.HINT_MAX_DISTANCE))

        GameBotLogic.logger.info("GameBotLogic.start. secretNumber={} hintLowerBound={} hintUpperBound={}".format(self.secretNumber, 
            self.hintLowerBound, self.hintUpperBound))
        
    def getLowerHint(self) -> int:
        return self.hintLowerBound

    def getUpperHint(self) -> int:
        return self.hintUpperBound

    def getCount(self) -> int:
        return self.count

    def getInstance() -> "GameBotLogic":
        if GameBotLogic._instance is None:
            GameBotLogic()
        return GameBotLogic._instance

    def checkAnswer(self, answer: int) -> CheckResult:
        self.count += 1
        GameBotLogic.logger.info("GameBotLogic.checkAnswer. answer={} upperHint={} lowerHint={}".format(answer, self.hintUpperBound, self.hintLowerBound))
        if answer < self.hintLowerBound or answer > self.hintUpperBound:
            return CheckResult.INVALID
        elif answer < self.secretNumber: 
            self.hintLowerBound = answer
            return CheckResult.GREATER_THAN
        elif answer > self.secretNumber: 
            self.hintUpperBound = answer
            return CheckResult.LESS_THAN
        return CheckResult.EQUAL

class GameUserLogic:
    MAX_RAND = 1000
    MIN_RAND = 0

    _instance = None

    logger = Logger(__name__).getInstance()
    
    def __init__(self) -> None:
        GameUserLogic._instance = self

        self.lowerBound = -1
        self.upperBound = -1
        self.guessNumber = -1
        self.isValid = False

    def start(self) -> None:
        self.lowerBound = GameUserLogic.MIN_RAND
        self.upperBound = GameUserLogic.MAX_RAND
        self.isValid = False

        self.guess()

        GameUserLogic.logger.info("GameUserLogic.start. guessNumber={} lowerBound={} upperBound={}".format(self.guessNumber, 
            self.lowerBound, self.upperBound))

    def guess(self) -> bool:
        if self.lowerBound > self.upperBound:
            return False
        GameUserLogic.logger.info("GameUserLogic.guess. lowerBound={} upperBound={}".format(self.lowerBound, self.upperBound))
        self.guessNumber = random.randint(self.lowerBound, self.upperBound)
        return True

    def updateLower(self) -> None:
        self.lowerBound = self.guessNumber + 1

    def updateUpper(self) -> None:
        self.upperBound = self.guessNumber - 1

    def setValid(self, isValid: bool) -> None:
        self.isValid = isValid

    def getGuessNumber(self) -> int:
        return self.guessNumber
    
    def getInstance() -> "GameUserLogic":
        if GameUserLogic._instance is None:
            GameUserLogic()
        return GameUserLogic._instance