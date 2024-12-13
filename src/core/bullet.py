import pygame
import pygame.gfxdraw

from core.space_object import INF, SpaceObject

BULLET_IMAGE = pygame.Surface((4, 4), pygame.SRCALPHA)
pygame.gfxdraw.box(BULLET_IMAGE, BULLET_IMAGE.get_rect(), (255, 255, 255))


class Bullet(SpaceObject):
    """
    Class representing a bullet in the game.
    """

    def __init__(self, ttl=50, **kwargs):
        super().__init__(**kwargs, image=BULLET_IMAGE)
        self._ttl = ttl

    @property
    def ttl(self):
        return self._ttl

    def update(self, area=(INF, INF)):
        super().update(area)
        if self._ttl > 0:
            self._ttl -= 1
        else:
            self.kill()
