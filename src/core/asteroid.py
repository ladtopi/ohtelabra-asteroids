import random

import pygame
import pygame.gfxdraw

from core.space_object import SpaceObject
from graphics.colors import WHITE

IMAGES = [pygame.Surface((d, d), pygame.SRCALPHA) for d in [0, 30, 50, 70]]
for surf in IMAGES:
    d = surf.get_width()
    pygame.draw.circle(surf,
                       center=(d/2, d/2),
                       radius=d//2-1,
                       color=WHITE,
                       width=2)
ASTEROID_INIT_SIZE = 3
FRAGMENTS = 2
REWARDS = [0, 25, 100, 250]


class Asteroid(SpaceObject):
    """
    Class representing an asteroid in the game.
    """

    def __init__(self, level=ASTEROID_INIT_SIZE, **kwargs):
        super().__init__(
            **kwargs,
            image=IMAGES[level],
        )
        self.level = level
        self.reward = REWARDS[level]

    def _make_fragment(self):
        return Asteroid(position=self._position,
                        velocity=self._velocity.rotate(
                            random.uniform(-45, 45)) * random.uniform(1.0, 1.2),
                        level=self.level - 1,)

    def explode(self):
        """
        Explodes the asteroid into smaller fragments.
        """
        if self.level > 1:
            return [self._make_fragment() for _ in range(FRAGMENTS)]
        return []
