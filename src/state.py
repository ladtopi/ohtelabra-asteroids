import pygame

from asteroid import Asteroid
from constants import Event, FontFamily
from ship import Ship


class GameState:
    """
    Abstract base class for game states.
    """

    def __init__(self, display):
        self.display = display

    def handle_events(self, event_queue, key_ctrl):
        """
        Handle events for this state.
        """
        raise NotImplementedError

    def update(self, event_queue):
        """
        Update the state.
        """
        raise NotImplementedError

    def render(self):
        """
        Render the state.
        """
        raise NotImplementedError


class PlayingState(GameState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        w, h = self.display.get_size()
        self.objects = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.ship = Ship(x=w/2, y=h/2, display=self.display)
        asteroid1 = Asteroid(x=100, y=100, vx=0.05,
                             vy=0.25, display=self.display)
        asteroid2 = Asteroid(x=600, y=200, vx=-.12,
                             vy=.1, display=self.display)
        self.objects.add(self.ship)
        self.objects.add(asteroid1)
        self.objects.add(asteroid2)
        self.asteroids.add(asteroid1)
        self.asteroids.add(asteroid2)
        self.objects.draw(self.display)

    def handle_events(self, event_queue, key_ctrl):
        for event in event_queue.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = self.ship.fire()
                self.objects.add(bullet)
                self.bullets.add(bullet)

        pressed = key_ctrl.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.ship.rotate_right()
        if pressed[pygame.K_LEFT]:
            self.ship.rotate_left()
        if pressed[pygame.K_UP]:
            self.ship.thrust()

        self.display.fill((0, 0, 0))
        self.objects.draw(self.display)

    def update(self, event_queue):
        self.objects.update()

        for asteroid in pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True):
            frags = asteroid.explode()
            self.objects.add(*frags)
            self.asteroids.add(*frags)

        if pygame.sprite.spritecollide(self.ship, self.asteroids, True):
            event_queue.post(pygame.event.Event(Event.GAME_OVER))

        self.objects.draw(self.display)

    def render(self):
        self.display.fill((0, 0, 0))
        self.objects.draw(self.display)


class GameOverState(GameState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font = pygame.font.SysFont(FontFamily.SYS_MONO, 36)
        self.text = self.font.render("Game Over", True, (255, 0, 0))

    def handle_events(self, event_queue, key_ctrl):
        pass

    def update(self, event_queue):
        pass

    def render(self):
        self.display.fill((0, 0, 0))
        x = self.display.get_width() / 2 - self.text.get_width() / 2
        y = self.display.get_height() / 2 - self.text.get_height() / 2
        self.display.blit(self.text, (x, y))
