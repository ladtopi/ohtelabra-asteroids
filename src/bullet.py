import pygame
import pygame.gfxdraw

from space_object import SpaceObject

BULLET_IMAGE = pygame.Surface((2, 5), pygame.SRCALPHA)
pygame.gfxdraw.box(BULLET_IMAGE, BULLET_IMAGE.get_rect(), (255, 255, 255))


class Bullet(SpaceObject):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            image=BULLET_IMAGE,
        )
        self.ttl = 1000

    def update(self):
        super().update()
        if self.ttl > 0:
            self.ttl -= 1
        else:
            self.kill()
