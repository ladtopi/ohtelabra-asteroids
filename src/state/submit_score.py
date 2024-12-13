
import pygame
from pygame_textinput import TextInputManager, TextInputVisualizer
from draw import draw_centered_text
from game import Game
from leaderboard import Leaderboard, LeaderboardEntry
from .base import BaseGameState, GameState


class SubmitScoreState(BaseGameState):
    def __init__(self, game: Game, leaderboard: Leaderboard):
        super().__init__()
        self._game = game
        self._leaderboard = leaderboard
        self._name_input = TextInputVisualizer(
            manager=TextInputManager(
                validator=lambda x: x.isalnum() and len(x) <= 3),
            font_color=(255, 255, 255),
            cursor_color=(255, 255, 255),
            cursor_width=12)

    def reset(self):
        self._name_input.value = ""

    def handle_events(self, events):
        self._name_input.update(events)
        self._uppercase_input()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self._submit_score():
                        self.request_transition(GameState.MENU)

    def _uppercase_input(self):
        self._name_input.value = self._name_input.value.upper()

    def _submit_score(self):
        name = self._name_input.value
        if len(name) < 3:
            return False
        self._leaderboard.add_entry(
            LeaderboardEntry(name=name,
                             score=self._game.score,
                             bullets_used=self._game.bullets_used))
        return True

    def draw(self, screen):
        screen.fill((0, 0, 0))
        rect = draw_centered_text(
            screen, "Name", size=36, color=(255, 0, 0))
        screen.blit(self._name_input.surface, rect.move(0, 50))
