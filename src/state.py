import pygame

from asteroid import Asteroid
from constants import Event
from ship import Ship


class GameState:
    def __init__(self, display):
        self.display = display
        self.objects = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.ship = None
        self.score = None
        self.ships_remaining = None
        self.reset()

    def reset(self):
        self.objects.empty()
        self.bullets.empty()
        self.asteroids.empty()

        self.score = 0
        self.ships_remaining = 3

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

    def fire_ship(self):
        bullet = self.ship.fire()
        self.objects.add(bullet)
        self.bullets.add(bullet)

    def thrust_ship(self):
        self.ship.thrust()

    def rotate_ship_right(self):
        self.ship.rotate_right()

    def rotate_ship_left(self):
        self.ship.rotate_left()

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
