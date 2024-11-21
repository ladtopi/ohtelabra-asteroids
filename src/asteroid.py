import pygame
import pygame.gfxdraw

from space_object import SpaceObject

ASTEROID_IMAGE = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.gfxdraw.filled_circle(ASTEROID_IMAGE, 20, 20, 19, (180, 220, 220))


class Asteroid(SpaceObject):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            image=ASTEROID_IMAGE,
            acceleration=0.005,
            friction=0
        )
