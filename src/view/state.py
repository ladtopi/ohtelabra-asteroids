from enum import Enum, auto


class GameViewState(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    SUBMIT_SCORE = auto()
