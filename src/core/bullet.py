import pygame
import pygame.gfxdraw

from core.space_object import INF, SpaceObject
from graphics.colors import WHITE

BULLET_IMAGE = pygame.Surface((4, 4), pygame.SRCALPHA)
pygame.gfxdraw.box(BULLET_IMAGE, BULLET_IMAGE.get_rect(), WHITE)


class Bullet(SpaceObject):
    """
    Class representing a bullet in the game.
    """

    def __init__(self, ttl=.75, **kwargs):
        super().__init__(**kwargs, image=BULLET_IMAGE)
        self._ttl = ttl

    @property
    def ttl(self):
        """
        Time to live (in seconds) for the bullet.
        """
        return self._ttl

    def update(self, area=(INF, INF), time_delta=1.0):
        super().update(area=area, time_delta=time_delta)
        if self._ttl > 0:
            self._ttl -= time_delta
        else:
            self.kill()
