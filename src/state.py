from enum import Enum, auto
import pygame
from collisions import CollisionChecker
from events import EVENT_SPAWN_ASTEROID_WAVE, EVENT_SPAWN_SHIP, EventQueue
from world import World


class BaseGameState:
    def enter(self):
        pass

    def cleanup(self):
        pass

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass

    def handle_keys(self, keys):
        pass

    def update(self):
        pass


class PlayingState(BaseGameState):
    def __init__(self):
        self._world = World(CollisionChecker(), EventQueue(),
                            pygame.display.get_surface())

    def handle_event(self, event):
        if event.type == EVENT_SPAWN_SHIP:
            self._world.spawn_ship()
        if event.type == EVENT_SPAWN_ASTEROID_WAVE:
            self._world.spawn_asteroid_wave()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._world.fire_ship()
            if event.key == pygame.K_RETURN and self._world.is_game_over():
                self._world.reset()
            if event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:
                self._world.reset()
            if event.key == pygame.K_d and event.mod & pygame.KMOD_CTRL:
                self._world.nuke_asteroids()

    def handle_keys(self, keys):
        if keys[pygame.K_UP]:
            self._world.thrust_ship()
        if keys[pygame.K_RIGHT]:
            self._world.rotate_ship_right()
        if keys[pygame.K_LEFT]:
            self._world.rotate_ship_left()

    def update(self):
        self._world.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self._world.objects.draw(screen)
        self.render_lives(screen)
        self.render_bullets(screen)
        self.render_asteroids(screen)
        self.render_score(screen)
        self.render_game_over(screen)

    def render_lives(self, screen):
        font = pygame.font.SysFont(None, 24)
        text = font.render(
            f"Ships: {self._world.ships_remaining}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def render_bullets(self, screen):
        font = pygame.font.SysFont(None, 24)
        text = font.render(
            f"Bullets: {self._world.bullets_remaining}", True, (255, 255, 255))
        screen.blit(text, (10, 34))

    def render_asteroids(self, screen):
        # conveneince for development
        font = pygame.font.SysFont(None, 24)
        text = font.render(
            f"Asteroids: {self._world.asteroids_remaining}", True, (0, 0, 255))
        screen.blit(text, (screen.get_width() //
                           2 - text.get_width() // 2, 10))

    def render_score(self, screen):
        font = pygame.font.SysFont(None, 24)
        text = font.render(
            f"Score: {self._world.score}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() -
                           10 - text.get_width(), 10))

    def render_game_over(self, screen):
        if self._world.is_game_over():
            font_lg = pygame.font.SysFont(None, 36)
            font_md = pygame.font.SysFont(None, 24)
            game_over_text = font_lg.render("Game Over", True, (255, 0, 0))
            continue_text = font_md.render(
                "Press ENTER to start a new game", True, (255, 255, 255))
            x = screen.get_width() / 2 - game_over_text.get_width() / 2
            y = screen.get_height() / 2 - game_over_text.get_height() / 2
            screen.blit(game_over_text, (x, y))
            x = screen.get_width() / 2 - continue_text.get_width() / 2
            y += game_over_text.get_height()
            screen.blit(continue_text, (x, y))


class GameState(Enum):
    PLAYING = auto()
