import pygame

from events import EventQueue
from keyboard import Keyboard
from state import BaseGameState, GameState


class GameLoop:
    """
    The main game loop that handles events, updates the game state, and renders
    the game.
    """

    def __init__(self,
                 state_map: dict[GameState, BaseGameState],
                 starting_state: GameState,
                 screen: pygame.Surface,
                 event_queue=EventQueue(),
                 keyboard=Keyboard(),
                 frame_callback=lambda: None):
        self._screen = screen
        self._frame_cb = frame_callback
        self._state_map = state_map
        self._state = state_map[starting_state]
        self._event_queue = event_queue
        self._keyboard = keyboard
        self._clock = pygame.time.Clock()
        self._running = False

    @property
    def state(self):
        return self._state

    @property
    def running(self):
        return self._running

    def run(self):
        """
        Runs the main game loop, handling events, updating the game state, and
        rendering the game.
        """
        self._running = True
        while self._running:
            self._handle_events()
            self._handle_keys()
            if state := self._state.next():
                self._move_to(state)
            self._state.update()
            self._state.draw(self._screen)
            self._frame_cb()
            self._clock.tick(60)

    def quit(self):
        """
        Stops the game loop.
        """
        self._running = False

    def _move_to(self, state):
        self._state = self._state_map[state]
        self._state.enter()

    def _handle_events(self):
        events = self._event_queue.get()
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
        self._state.handle_events(events)

    def _handle_keys(self):
        keys = self._keyboard.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self._running = False
        else:
            self._state.handle_keys(keys)
