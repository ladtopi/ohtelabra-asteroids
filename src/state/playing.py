
import pygame

from core import Game
from events import EVENT_SPAWN_ASTEROID_WAVE, EVENT_SPAWN_SHIP
from graphics import draw_centered_text, draw_text

from .base import BaseGameState, GameState


class PlayingState(BaseGameState):
    def __init__(self, game: Game):
        super().__init__()
        self._game = game

    def handle_events(self, events):
        for event in events:
            if event.type == EVENT_SPAWN_SHIP:
                self._game.spawn_ship()
            if event.type == EVENT_SPAWN_ASTEROID_WAVE:
                self._game.spawn_asteroid_wave()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._game.fire_ship()
                if event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:
                    self._game.reset()
                if event.key == pygame.K_d and event.mod & pygame.KMOD_CTRL:
                    self._game.nuke_asteroids()

    def handle_keys(self, keys):
        if keys[pygame.K_UP]:
            self._game.thrust_ship()
        if keys[pygame.K_RIGHT]:
            self._game.rotate_ship_right()
        if keys[pygame.K_LEFT]:
            self._game.rotate_ship_left()

    def update(self):
        self._game.update()
        if self._game.is_game_over():
            self.request_transition(GameState.GAME_OVER)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self._game.objects.draw(screen)
        self.render_lives(screen)
        self.render_bullets(screen)
        self.render_asteroids(screen)
        self.render_score(screen)

    def render_lives(self, screen):
        draw_text(
            screen, f"Ships: {self._game.ships_remaining}", (10, 10))

    def render_bullets(self, screen):
        draw_text(
            screen, f"Bullets: {self._game.bullets_remaining}", (10, 34))

    def render_asteroids(self, screen):
        # conveneince for development
        draw_centered_text(
            screen, f"Asteroids: {self._game.asteroids_remaining}", 10)

    def render_score(self, screen):
        draw_text(screen, f"Score: {self._game.score}", (-10, 10))
