
import pygame

from core import Game
from graphics import draw_centered_text, draw_centered_text_below
from graphics.colors import BLACK, GREEN

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
        screen.fill(BLACK)
        rect = draw_centered_text(
            screen, "Game Over", size="lg", color=(255, 0, 0))
        rect = draw_centered_text_below(
            screen, f"Score: {self._game.score}", rect, color=GREEN, margin=20)
        rect = draw_centered_text_below(
            screen, f"Bullets used: {self._game.bullets_used}", rect, color=GREEN)
        rect = draw_centered_text_below(
            screen, "Press ENTER to start a new game", rect, margin=20)
        rect = draw_centered_text_below(
            screen, "Or SPACE to submit your score", rect)
