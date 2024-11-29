import random
import pygame

from asteroid import Asteroid
from cartesian import random_coords
from events import EVENT_SPAWN_ASTEROID_WAVE, EVENT_SPAWN_SHIP
from ship import Ship


INITIAL_WAVE_SIZE = 3


class GameState:
    def __init__(self, collision_checker, event_queue, display):
        self.collision_checker = collision_checker
        self.event_queue = event_queue
        self.display = display
        self.objects = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.ship = None
        self.score = None
        self.ships_remaining = None
        self.waves = None

    @property
    def asteroids_remaining(self):
        return len(self.asteroids)

    def reset(self):
        self.objects.empty()
        self.bullets.empty()
        self.asteroids.empty()

        self.score = 0
        self.ships_remaining = 3
        self.waves = 0

        self.spawn_ship()
        self.spawn_asteroid_wave()

        return self

    def spawn_asteroid(self, x=0, y=0, vx=0, vy=0, size=3):
        asteroid = Asteroid(x=x, y=y, vx=vx, vy=vy,
                            display=self.display, size=size)
        self.objects.add(asteroid)
        self.asteroids.add(asteroid)
        return asteroid

    def spawn_asteroid_wave(self):
        self.waves += 1
        asteroids = []
        for _ in range(INITIAL_WAVE_SIZE + (self.waves // 2)):
            ship_x, ship_y = self.ship.position
            w, h = self.display.get_size()
            center = random_coords((w, h), (ship_x, ship_y, 0, 0), 80)
            vx = random.uniform(-0.20, 0.20)
            vy = random.uniform(-0.20, 0.20)
            asteroids.append(self.spawn_asteroid(*center, vx=vx, vy=vy))
        return asteroids

    def spawn_ship(self):
        if self.ship and self.ship.alive():
            return
        w, h = self.display.get_size()
        self.ship = Ship(x=w/2, y=h/2, display=self.display)
        self.objects.add(self.ship)
        return self.ship

    def fire_ship(self):
        bullet = self.ship.fire()
        self.objects.add(bullet)
        self.bullets.add(bullet)
        return bullet

    def thrust_ship(self):
        self.ship.thrust()

    def rotate_ship_right(self):
        self.ship.rotate_right()

    def rotate_ship_left(self):
        self.ship.rotate_left()

    def is_game_over(self):
        return self.ships_remaining < 1

    def kill_ship(self):
        self.ship.kill()
        self.ships_remaining -= 1
        if not self.is_game_over():
            self.event_queue.defer(EVENT_SPAWN_SHIP, 1000)

    def kill_bullet(self, bullet):
        bullet.kill()

    def explode_asteroid(self, asteroid):
        asteroid.kill()
        self.score += asteroid.reward
        frags = asteroid.explode()
        self.objects.add(*frags)
        self.asteroids.add(*frags)
        if len(self.asteroids) == 0:
            self.event_queue.defer(EVENT_SPAWN_ASTEROID_WAVE, 1000)
        return frags

    def nuke_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.kill()
        self.event_queue.defer(EVENT_SPAWN_ASTEROID_WAVE, 1000)

    def handle_collisions(self):
        for bullet in self.bullets:
            if asteroid := self.collision_checker.get_collision(bullet, self.asteroids):
                self.kill_bullet(bullet)
                self.explode_asteroid(asteroid)

        if self.ship.alive():
            if asteroid := self.collision_checker.get_collision(self.ship, self.asteroids):
                self.kill_ship()
                self.explode_asteroid(asteroid)

    def update(self):
        self.handle_collisions()
        self.objects.update()
