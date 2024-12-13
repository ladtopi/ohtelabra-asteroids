from enum import Enum, auto
import pygame
from pygame_textinput import TextInputManager, TextInputVisualizer
from events import EVENT_SPAWN_ASTEROID_WAVE, EVENT_SPAWN_SHIP
from leaderboard import Leaderboard, LeaderboardEntry
from game import Game
from draw import draw_centered_text, draw_centered_text_below, draw_text, draw_text_below


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

    def handle_events(self, events):
        pass

    def handle_keys(self, keys):
        pass

    def update(self):
        pass


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


class GameOverState(BaseGameState):
    def __init__(self, game: Game):
        super().__init__()
        self._game = game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
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


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    SUBMIT_SCORE = auto()
