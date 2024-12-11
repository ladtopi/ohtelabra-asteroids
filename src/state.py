from enum import Enum, auto
import pygame
from collisions import CollisionChecker
from events import EVENT_SPAWN_ASTEROID_WAVE, EVENT_SPAWN_SHIP, EventQueue
from world import World
from draw import draw_centered_text, draw_centered_text_below, draw_text


class BaseGameState:
    def __init__(self):
        self._next = None

    def request_transition(self, state):
        self._next = state

    def enter(self):
        self._next = None
        self.reset()

    def reset(self):
        pass

    def next(self):
        return self._next

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass

    def handle_keys(self, keys):
        pass

    def update(self):
        pass


class MenuState(BaseGameState):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.request_transition(GameState.PLAYING)

    def next(self):
        return self._next

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title_rect = draw_centered_text(screen, "Asteroids", size=36)
        draw_centered_text_below(screen, "Press ENTER to start", title_rect)


class PlayingState(BaseGameState):
    def __init__(self):
        super().__init__()
        self._world = World(CollisionChecker(), EventQueue(),
                            pygame.display.get_surface())

    def reset(self):
        self._world.reset()

    def handle_event(self, event):
        if event.type == EVENT_SPAWN_SHIP:
            self._world.spawn_ship()
        if event.type == EVENT_SPAWN_ASTEROID_WAVE:
            self._world.spawn_asteroid_wave()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._world.fire_ship()
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
        if self._world.is_game_over():
            self.request_transition(GameState.GAME_OVER)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self._world.objects.draw(screen)
        self.render_lives(screen)
        self.render_bullets(screen)
        self.render_asteroids(screen)
        self.render_score(screen)

    def render_lives(self, screen):
        draw_text(
            screen, f"Ships: {self._world.ships_remaining}", (10, 10))

    def render_bullets(self, screen):
        draw_text(
            screen, f"Bullets: {self._world.bullets_remaining}", (10, 34))

    def render_asteroids(self, screen):
        # conveneince for development
        draw_centered_text(
            screen, f"Asteroids: {self._world.asteroids_remaining}", 10)

    def render_score(self, screen):
        draw_text(screen, f"Score: {self._world.score}", (-10, 10))


class GameOverState(BaseGameState):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.request_transition(GameState.PLAYING)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title_rect = draw_centered_text(
            screen, "Game Over", size=36, color=(255, 0, 0))
        draw_centered_text_below(
            screen, "Press ENTER to start a new game", title_rect)


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
