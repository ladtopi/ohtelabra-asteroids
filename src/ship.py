import pygame
import pygame.gfxdraw

from bullet import Bullet
from space_object import SpaceObject

SHIP_SIZE = 40
SHIP_IMAGE = pygame.Surface((SHIP_SIZE, SHIP_SIZE), pygame.SRCALPHA)
pygame.gfxdraw.filled_trigon(SHIP_IMAGE, 0, SHIP_SIZE, SHIP_SIZE //
                             2, 0, SHIP_SIZE, SHIP_SIZE, (255, 255, 255))
SHIP_MAX_SPEED = 2


class Ship(SpaceObject):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            image=SHIP_IMAGE,
            acceleration=0.002,
            friction=0.0005,
        )

    def thrust(self):
        if self.velocity.length() < SHIP_MAX_SPEED:
            self.velocity += pygame.Vector2(
                0, (-self.acceleration)).rotate(self.angle)

    def fire(self):
        v = pygame.Vector2(0, -1.25).rotate(self.angle)
        x, y = self.position
        return Bullet(
            x=x,
            y=y,
            vx=self.velocity.x + v.x,
            vy=self.velocity.y + v.y,
            angle=self.angle,
            display=self.display,
        )
