import pygame
import pygame.gfxdraw

from space_object import SpaceObject

ASTEROID_IMAGE = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.gfxdraw.filled_circle(ASTEROID_IMAGE, 20, 20, 19, (180, 220, 220))


class Asteroid(SpaceObject):
    def __init__(self, x=0, y=0, v=pygame.Vector2(0, 0), screen_size=(800, 600)):
        super().__init__(
            x=x,
            y=y,
            screen_size=screen_size,
            image=ASTEROID_IMAGE,
            velocity=v,
            position=pygame.Vector2(x, y),
            acceleration=0.005,
            friction=0
        )
