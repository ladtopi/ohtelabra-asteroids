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
        """
        Requests transition to the specifieed state.

        Args:
            state: The state to transition to.
        """
        self._next = state

    def enter(self):
        """
        Called when the state is entered.
        """
        self._next = None
        self.reset()

    def reset(self):
        """
        Resets the state (on entering)
        """
        # Implement as required

    def next(self):
        """
        Returns the next state to transition to.
        """
        return self._next

    def draw(self, screen):
        """
        Draws the state tot the screen.

        Args:
            screen: The pygame Surface to draw to.
        """
        # Implement as required

    def handle_events(self, events):
        """
        Handles events.

        Args:
            events: A list of pygame events.
        """
        # Implement as required

    def handle_keys(self, keys):
        """
        Handles key presses.

        Args:
            keys: A dictionary of key states.
        """
        # Implement as required

    def update(self, time_delta):
        """
        Routine for updating the state.
        """
        # Implement as required
