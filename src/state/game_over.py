
import pygame

from core import Game
from graphics import draw_centered_text, draw_centered_text_below

from .base import BaseGameState, GameState


class GameOverState(BaseGameState):
    def __init__(self, game: Game):
        super().__init__()
        self._game = game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._game.reset()
                    self.request_transition(GameState.PLAYING)
                if event.key == pygame.K_SPACE:
                    self.request_transition(GameState.SUBMIT_SCORE)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        rect = draw_centered_text(
            screen, "Game Over", size=36, color=(255, 0, 0))
        rect = draw_centered_text_below(
            screen, f"Score: {self._game.score}", rect)
        rect = draw_centered_text_below(
            screen, f"Bullets used: {self._game.bullets_used}", rect)
        rect = draw_centered_text_below(
            screen, "Press ENTER to start a new game", rect)
        rect = draw_centered_text_below(
            screen, "Or SPACE to submit your score to leaderboard", rect)
