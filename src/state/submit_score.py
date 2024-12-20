
import pygame
from pygame_textinput import TextInputManager, TextInputVisualizer

from core import Game
from graphics import draw_centered_text
from graphics.colors import BLACK, WHITE, GREEN
from leaderboard import Leaderboard, LeaderboardEntry

from .base import BaseGameState, GameState


class SubmitScoreState(BaseGameState):
    def __init__(self, game: Game, leaderboard: Leaderboard):
        super().__init__()
        self._game = game
        self._leaderboard = leaderboard
        self._name_input = TextInputVisualizer(
            manager=TextInputManager(
                validator=lambda x: x == "" or x.isalnum() and len(x) <= 3),
            font_color=WHITE,
            cursor_color=WHITE,
            cursor_width=12)

    def handle_events(self, events):
        self._name_input.update(events)
        self._uppercase_input()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._submit_score()

    def _uppercase_input(self):
        self._name_input.value = self._name_input.value.upper()

    def _submit_score(self):
        name = self._name_input.value
        if len(name) < 3:
            return
        self._leaderboard.add_entry(
            LeaderboardEntry(name=name,
                             score=self._game.score,
                             bullets_used=self._game.bullets_used))
        self.request_transition(GameState.MENU)

    def draw(self, screen):
        screen.fill(BLACK)
        rect = draw_centered_text(
            screen, "Name", size=36, color=GREEN)
        screen.blit(self._name_input.surface, rect.move(0, 50))
