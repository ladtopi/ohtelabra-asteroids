import pygame
from state import GameOverState, GameState, MenuState, PlayingState


class GameLoop:
    """
    The main game loop that handles events, updates the game state, and renders the game.
    """

    def __init__(self, state=GameState.MENU):
        self._state_map = {
            GameState.MENU: MenuState(),
            GameState.PLAYING: PlayingState(),
            GameState.GAME_OVER: GameOverState(),
        }
        self._state = self._state_map[state]
        self._running = True

    def run(self):
        """
        Runs the main game loop, handling events, updating the game state, and rendering the game.
        """
        while self._running:
            self._handle_events()
            self._handle_keys()
            if state := self._state.next():
                self._move_to(state)
            self._state.update()
            self._state.draw(pygame.display.get_surface())
            pygame.display.flip()

    def _move_to(self, state):
        self._state = self._state_map[state]
        self._state.enter()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            else:
                self._state.handle_event(event)

    def _handle_keys(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self._running = False
        else:
            self._state.handle_keys(pygame.key.get_pressed())
