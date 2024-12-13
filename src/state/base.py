from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    SUBMIT_SCORE = auto()


class BaseGameState:
    def __init__(self):
        self._next = None

    def request_transition(self, state):
        self._next = state

    def enter(self):
        self._next = None
        self.reset()

    def reset(self):
        pass

    def next(self):
        return self._next

    def draw(self, screen):
        pass

    def handle_events(self, events):
        pass

    def handle_keys(self, keys):
        pass

    def update(self):
        pass
