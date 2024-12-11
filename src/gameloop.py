import pygame
from db import Database
from leaderboard import Leaderboard
from score import Score
from state import GameOverState, GameState, MenuState, PlayingState, SubmitScoreState


class GameLoop:
    """
    The main game loop that handles events, updates the game state, and renders the game.
    """

    def __init__(self, state=GameState.MENU):
        self._score = Score()
        self._leaderboard = Leaderboard(Database())
        self._state_map = {
            GameState.MENU: MenuState(self._leaderboard),
            GameState.PLAYING: PlayingState(self._score),
            GameState.GAME_OVER: GameOverState(self._score),
            GameState.SUBMIT_SCORE: SubmitScoreState(self._score, self._leaderboard),
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
        if pygame.event.get(eventtype=pygame.QUIT):
            self._running = False
        else:
            self._state.handle_events(pygame.event.get())

    def _handle_keys(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self._running = False
        else:
            self._state.handle_keys(pygame.key.get_pressed())
