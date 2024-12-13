
import pygame

from graphics import (draw_centered_text, draw_centered_text_below, draw_text,
                      draw_text_below)
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
        screen.fill((0, 0, 0))
        title_rect = draw_centered_text(screen, "Asteroids", size=36)
        draw_centered_text_below(screen, "Press ENTER to start", title_rect)
        self.draw_leaderboard(screen)

    def draw_leaderboard(self, screen):
        rect = draw_text(screen, "Leaderboard", (-10, 10))
        for entry in self._leaderboard.get_top_10():
            rect = draw_text_below(
                screen, f"{entry.name}: {entry.score}", rect, margin=10)
