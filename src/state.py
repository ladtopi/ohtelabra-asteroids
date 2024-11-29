import pygame

from asteroid import Asteroid
from constants import EVENT_SPAWN_SHIP
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

        self.spawn_ship()
        self.spawn_asteroid(x=100, y=100, vx=0.05, vy=0.25)
        self.spawn_asteroid(x=600, y=200, vx=-.12, vy=.1)

    def spawn_asteroid(self, x, y, vx, vy):
        asteroid = Asteroid(x=x, y=y, vx=vx, vy=vy, display=self.display)
        self.objects.add(asteroid)
        self.asteroids.add(asteroid)

    def spawn_ship(self):
        if self.ship and self.ship.alive():
            return
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

    def kill_ship(self):
        self.ship.kill()
        self.ships_remaining -= 1

    def kill_bullet(self, bullet):
        bullet.kill()

    def explode_asteroid(self, asteroid):
        asteroid.kill()
        self.score += asteroid.reward
        frags = asteroid.explode()
        self.objects.add(*frags)
        self.asteroids.add(*frags)

    def update(self):
        for asteroid, bullets in pygame.sprite.groupcollide(self.asteroids, self.bullets, 0, 0).items():
            # self.explode_asteroid(asteroid)
            self.explode_asteroid(asteroid)
            for bullet in bullets:
                self.kill_bullet(bullet)

        if self.ship.alive():
            if asteroid := pygame.sprite.spritecollideany(self.ship, self.asteroids):
                self.kill_ship()
                self.explode_asteroid(asteroid)
                if not self.is_game_over():
                    pygame.time.set_timer(EVENT_SPAWN_SHIP, 1000, loops=1)

        self.objects.update()

    def is_game_over(self):
        return self.ships_remaining == 0
