import pygame
import pygame.gfxdraw

from space_object import SpaceObject

SHIP_SIZE = 40
SHIP_IMAGE = pygame.Surface((SHIP_SIZE, SHIP_SIZE), pygame.SRCALPHA)
pygame.gfxdraw.filled_trigon(SHIP_IMAGE, 0, SHIP_SIZE, SHIP_SIZE //
                             2, 0, SHIP_SIZE, SHIP_SIZE, (255, 255, 255))


class Ship(SpaceObject):
    def __init__(self, x=0, y=0, display=None):
        super().__init__(
            x=x,
            y=y,
            display=display,
            image=SHIP_IMAGE,
            velocity=pygame.Vector2(0, 0),
            position=pygame.Vector2(x, y),
            acceleration=0.002,
            friction=0.0005,
            angle=0
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
