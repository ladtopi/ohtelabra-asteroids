import pygame

from asteroid import Asteroid
from constants import Event
from ship import Ship


class GameState:
    def __init__(self, display):
        self.score = 0
        self.ships_remaining = 3

        self.display = display

        self.objects = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        self.replace_ship()

        asteroid1 = Asteroid(x=100, y=100, vx=0.05,
                             vy=0.25, display=self.display)
        asteroid2 = Asteroid(x=600, y=200, vx=-.12,
                             vy=.1, display=self.display)
        self.objects.add(self.ship)
        self.objects.add(asteroid1)
        self.objects.add(asteroid2)
        self.asteroids.add(asteroid1)
        self.asteroids.add(asteroid2)

    def replace_ship(self):
        w, h = self.display.get_size()
        self.ship = Ship(x=w/2, y=h/2, display=self.display)
        self.objects.add(self.ship)

    def handle_events(self, event_queue, key_ctrl):
        for event in event_queue.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = self.ship.fire()
                self.objects.add(bullet)
                self.bullets.add(bullet)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.is_game_over():
                pygame.event.post(pygame.event.Event(Event.START_NEW_GAME))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and key_ctrl.get_mods() & pygame.KMOD_CTRL:
                # print("ctrl-r pressed")
                # convenience feature for development
                pygame.event.post(pygame.event.Event(Event.START_NEW_GAME))
            if event.type == Event.REPLACE_SHIP:
                self.replace_ship()

        pressed = key_ctrl.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.ship.rotate_right()
        if pressed[pygame.K_LEFT]:
            self.ship.rotate_left()
        if pressed[pygame.K_UP]:
            self.ship.thrust()

    def update(self):
        self.objects.update()

        for asteroid in pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True):
            self.score += asteroid.reward
            frags = asteroid.explode()
            self.objects.add(*frags)
            self.asteroids.add(*frags)

        if self.ship.alive():
            if asteroids := pygame.sprite.spritecollide(self.ship, self.asteroids, True):
                self.ship.kill()
                self.ships_remaining -= 1
                if self.ships_remaining > 0:
                    pygame.time.set_timer(Event.REPLACE_SHIP, 1000, loops=1)
                self.score += asteroids[0].reward
                frags = asteroids[0].explode()
                self.objects.add(*frags)
                self.asteroids.add(*frags)

    def is_game_over(self):
        return self.ships_remaining == 0
