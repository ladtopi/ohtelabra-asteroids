import pygame

from collisions import CollisionChecker
from config import config
from core.game import Game
from db import Database
from leaderboard import Leaderboard
from loop import GameLoop
from state.base import GameState
from state.game_over import GameOverState
from state.menu import MenuState
from state.playing import PlayingState
from state.submit_score import SubmitScoreState


class Pysteroids:
    def __init__(self, w=config.window_width, h=config.window_height):
        pygame.init()
        pygame.display.set_caption("Pysteroids")
        pygame.display.set_mode((w, h))
        self._loop = self._build_loop()

    def _build_loop(self):
        screen = pygame.display.get_surface()
        game = Game(collision_checker=CollisionChecker(), display=screen)
        leaderboard = Leaderboard(Database())
        state_map = {
            GameState.MENU: MenuState(leaderboard),
            GameState.PLAYING: PlayingState(game),
            GameState.GAME_OVER: GameOverState(game),
            GameState.SUBMIT_SCORE: SubmitScoreState(game, leaderboard),
        }

        return GameLoop(
            state_map=state_map,
            screen=screen,
            starting_state=GameState.MENU,
            frame_callback=pygame.display.flip)

    def run(self):
        self._loop.run()
