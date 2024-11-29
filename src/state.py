import pygame

from asteroid import Asteroid
from events import EVENT_SPAWN_SHIP
from ship import Ship


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
        if self.should_respawn():
            self.event_queue.defer(EVENT_SPAWN_SHIP, 1000)

    def kill_bullet(self, bullet):
        bullet.kill()

    def explode_asteroid(self, asteroid):
        asteroid.kill()
        self.score += asteroid.reward
        frags = asteroid.explode()
        self.objects.add(*frags)
        self.asteroids.add(*frags)

    def update(self):
        for bullet in self.bullets:
            if asteroid := self.collision_checker.get_collision(bullet, self.asteroids):
                self.kill_bullet(bullet)
                self.explode_asteroid(asteroid)

        if self.ship.alive():
            if asteroid := self.collision_checker.get_collision(self.ship, self.asteroids):
                self.kill_ship()
                self.explode_asteroid(asteroid)

        self.objects.update()

    def should_respawn(self):
        return not self.ship.alive() and not self.is_game_over()

    def is_game_over(self):
        return self.ships_remaining == 0
