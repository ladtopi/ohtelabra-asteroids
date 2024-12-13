import random

import pygame

from cartesian import random_coords
from events import EVENT_SPAWN_ASTEROID_WAVE, EVENT_SPAWN_SHIP, EventQueue

from .asteroid import Asteroid
from .bullet import Bullet
from .ship import Ship

INITIAL_WAVE_SIZE = 3


class Game:
    """
    Holds and manages the game state.
    """

    def __init__(self, collision_checker, display, event_queue=EventQueue()):
        self.collision_checker = collision_checker
        self.event_queue = event_queue
        self.display = display
        self.objects = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.ship = None

        self.reset()

    @property
    def asteroids_remaining(self):
        return len(self.asteroids)

    @property
    def bullets_remaining(self):
        return self.ship.bullets_remaining if self.ship and self.ship.alive() else 0

    def reset(self):
        """
        Resets the game state to the initial state.
        """
        self.objects.empty()
        self.bullets.empty()
        self.asteroids.empty()

        self.score = 0
        self.waves = 0
        self.bullets_used = 0
        self.ships_remaining = 3

        self.spawn_ship()
        self.spawn_asteroid_wave()

        return self

    def place_asteroid(self, asteroid: Asteroid):
        self.objects.add(asteroid)
        self.asteroids.add(asteroid)
        return asteroid

    def spawn_asteroid_wave(self):
        """
        Spawns a wave of asteroids with random positions and velocities.
        """
        self.waves += 1
        asteroids = []
        for _ in range(INITIAL_WAVE_SIZE + (self.waves // 2)):
            w, h = self.display.get_size()
            x, y = random_coords((w, h), (self.ship.x, self.ship.y, 0, 0), 100)
            vx = random.uniform(0.05, 0.25)
            vy = random.uniform(0.05, 0.25)
            if random.choice([True, False]):
                vx *= -1
            if random.choice([True, False]):
                vy *= -1
            asteroids.append(self.place_asteroid(
                Asteroid(position=(x, y), velocity=(vx, vy)))
            )
        return asteroids

    def spawn_ship(self):
        """
        Spawns a new ship in the game.
        """
        if self.ship and self.ship.alive():
            return None
        w, h = self.display.get_size()
        self.ship = Ship(position=(w/2, h/2))
        self.objects.add(self.ship)
        return self.ship

    def fire_ship(self):
        """
        Fires the ship's weapon.
        """
        bullet = self.ship.fire()
        if bullet:
            self.objects.add(bullet)
            self.bullets.add(bullet)
            self.bullets_used += 1
        return bullet

    def thrust_ship(self):
        """
        Applies thrust to the ship.
        """
        self.ship.thrust()

    def rotate_ship_right(self):
        """
        Rotates the ship to the right.
        """
        self.ship.rotate_right()

    def rotate_ship_left(self):
        """
        Rotates the ship to the left
        """
        self.ship.rotate_left()

    def is_game_over(self):
        return self.ships_remaining < 1

    def kill_ship(self):
        """
        Removes the current ship from the game and respawns a new one if one
        remains.
        """
        self.ship.kill()
        self.ships_remaining -= 1
        if not self.is_game_over():
            self.event_queue.defer(EVENT_SPAWN_SHIP, 1000)

    def kill_bullet(self, bullet: Bullet):
        """
        Removes a bullet from the game.
        """
        bullet.kill()

    def explode_asteroid(self, asteroid: Asteroid):
        """
        Explodes an asteroid into smaller fragments. Maintains the score.
        """
        asteroid.kill()
        self.score += asteroid.reward
        frags = asteroid.explode()
        self.objects.add(*frags)
        self.asteroids.add(*frags)
        if len(self.asteroids) == 0:
            self.event_queue.defer(EVENT_SPAWN_ASTEROID_WAVE, 1000)
        return frags

    def nuke_asteroids(self):
        """
        Removes all asteroids from the game. Useful for debugging.
        """
        for asteroid in self.asteroids:
            asteroid.kill()
        self.event_queue.defer(EVENT_SPAWN_ASTEROID_WAVE, 1000)

    def handle_collisions(self):
        """
        Checks for collisions between game objects and handles them.
        """
        for bullet in self.bullets:
            if asteroid := self.collision_checker.get_collision(bullet, self.asteroids):
                self.kill_bullet(bullet)
                self.explode_asteroid(asteroid)

        if self.ship.alive():
            if asteroid := self.collision_checker.get_collision(self.ship, self.asteroids):
                self.kill_ship()
                self.explode_asteroid(asteroid)

    def update(self):
        """
        Updates all objects (positions, velocities, etc) in the game.
        """
        self.handle_collisions()
        self.objects.update(self.display.get_size())
