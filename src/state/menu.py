
import pygame

from graphics import (draw_centered_text, draw_centered_text_below, draw_text,
                      draw_text_below)
from graphics.colors import BLACK, GREEN
from leaderboard import Leaderboard

from .base import BaseGameState, GameState


class MenuState(BaseGameState):
    def __init__(self, leaderboard: Leaderboard):
        super().__init__()
        self._leaderboard = leaderboard

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.request_transition(GameState.PLAYING)

    def next(self):
        return self._next

    def draw(self, screen):
        screen.fill(BLACK)
        title_rect = draw_centered_text(
            screen, "Asteroids", size="lg", color=(255, 0, 0))
        draw_centered_text_below(screen, "Press ENTER to start", title_rect)
        self._draw_leaderboard(screen)

    def _draw_leaderboard(self, screen):
        rect = draw_text(screen, "Leaderboard", (-10, 10), color=GREEN)
        for entry in self._leaderboard.get_top_list():
            rect = draw_text_below(
                screen,
                f"{entry.name}: {entry.score}",
                rect,
                margin=10,
                color=GREEN,)
