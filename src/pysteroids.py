import pygame

from collisions import CollisionChecker
from config import config
from core.game import Game
from db import Database
from leaderboard import Leaderboard
from loop import GameLoop
from view.state import GameViewState
from view.game_over import GameOverView
from view.menu import MenuView
from view.playing import PlayingView
from view.submit_score import SubmitScoreView


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
            GameViewState.MENU: MenuView(leaderboard),
            GameViewState.PLAYING: PlayingView(game),
            GameViewState.GAME_OVER: GameOverView(game),
            GameViewState.SUBMIT_SCORE: SubmitScoreView(game, leaderboard),
        }

        return GameLoop(
            state_map=state_map,
            screen=screen,
            starting_state=GameViewState.MENU,
            frame_callback=pygame.display.flip)

    def run(self):
        self._loop.run()
