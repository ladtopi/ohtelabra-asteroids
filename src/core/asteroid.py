import random
import pygame
import pygame.gfxdraw

from core.space_object import SpaceObject

ASTEROID_IMAGE = pygame.Surface((70, 70), pygame.SRCALPHA)
pygame.gfxdraw.filled_circle(ASTEROID_IMAGE, 35, 35, 34, (180, 220, 220))
ASTEROID_INIT_SIZE = 3
FRAGMENTS = 2

IMAGES = [pygame.transform.scale_by(ASTEROID_IMAGE, factor) for factor in [
    0, 0.33, 0.67, 1]]
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
