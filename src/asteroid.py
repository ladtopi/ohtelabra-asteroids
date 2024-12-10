import random
import pygame
import pygame.gfxdraw

from space_object import SpaceObject

ASTEROID_IMAGE = pygame.Surface((70, 70), pygame.SRCALPHA)
pygame.gfxdraw.filled_circle(ASTEROID_IMAGE, 35, 35, 34, (180, 220, 220))
ASTEROID_INIT_SIZE = 3


REWARDS = [0, 25, 100, 250]


class Asteroid(SpaceObject):
    """
    Class representing an asteroid in the game.
    """

    def __init__(self, size=ASTEROID_INIT_SIZE, **kwargs):
        super().__init__(
            **kwargs,
            image=pygame.transform.scale_by(
                ASTEROID_IMAGE, .6 ** (ASTEROID_INIT_SIZE-size)),
        )
        self.size = size
        self.reward = REWARDS[size]

    def explode(self):
        """
        Explodes the asteroid into smaller fragments.
        """
        frags = []
        if self.size > 1:
            for _ in range(2):
                v = self.velocity * random.uniform(1.0, 1.2)
                v = v.rotate(random.uniform(-45, 45))
                x, y = self.position
                frags.append(
                    Asteroid(
                        x=x,
                        y=y,
                        vx=v.x,
                        vy=v.y,
                        size=self.size - 1,
                        display=self.display,
                    ))
        return frags
