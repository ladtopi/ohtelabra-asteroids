import pygame
import pygame.gfxdraw

from bullet import Bullet
from space_object import SpaceObject

SHIP_SIZE = 40
SHIP_IMAGE = pygame.Surface((SHIP_SIZE, SHIP_SIZE), pygame.SRCALPHA)
pygame.gfxdraw.filled_trigon(SHIP_IMAGE, 0, SHIP_SIZE, SHIP_SIZE //
                             2, 0, SHIP_SIZE, SHIP_SIZE, (255, 255, 255))


class Ship(SpaceObject):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            image=SHIP_IMAGE,
            acceleration=0.002,
            friction=0.0005,
        )

    def rotate_right(self, degrees=1):
        if self.angle < degrees:
            self.angle += 360
        self.angle -= degrees
        self.image = pygame.transform.rotate(SHIP_IMAGE, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_left(self, degrees=1):
        if self.angle > 360 - degrees:
            self.angle -= 360
        self.angle += degrees
        self.image = pygame.transform.rotate(SHIP_IMAGE, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self):
        self.velocity += pygame.Vector2(
            0, (-self.acceleration)).rotate(-self.angle)

    def fire(self):
        v = pygame.Vector2(0, -.5).rotate(-self.angle)
        return Bullet(
            x=self.position.x,
            y=self.position.y,
            vx=self.velocity.x + v.x,
            vy=self.velocity.y + v.y,
            angle=self.angle,
            display=self.display,
        )
