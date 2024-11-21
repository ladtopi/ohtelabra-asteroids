import random
import pygame
import pygame.gfxdraw

from space_object import SpaceObject

ASTEROID_IMAGE = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.gfxdraw.filled_circle(ASTEROID_IMAGE, 20, 20, 19, (180, 220, 220))
ASTEROID_INIT_SIZE = 3


REWARDS = [0, 25, 100, 250]


class Asteroid(SpaceObject):
    def __init__(self, size=ASTEROID_INIT_SIZE, **kwargs):
        super().__init__(
            **kwargs,
            image=pygame.transform.scale_by(
                ASTEROID_IMAGE, .75 ** (ASTEROID_INIT_SIZE-size)),
        )
        self.size = size
        self.reward = REWARDS[size]

    def explode(self):
        frags = []
        if self.size > 1:
            for _ in range(2):
                v = self.velocity * random.uniform(.9, 1.1)
                v = v.rotate(random.uniform(-45, 45))
                frags.append(
                    Asteroid(
                        x=self.position.x,
                        y=self.position.y,
                        vx=v.x,
                        vy=v.y,
                        size=self.size - 1,
                        display=self.display,
                    ))
        return frags
