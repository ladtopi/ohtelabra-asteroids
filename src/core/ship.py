import pygame
import pygame.gfxdraw

from core.bullet import Bullet
from core.space_object import INF, UP, SpaceObject

SHIP_SIZE = 40
SHIP_IMAGE = pygame.Surface((SHIP_SIZE, SHIP_SIZE), pygame.SRCALPHA)
pygame.gfxdraw.filled_trigon(SHIP_IMAGE, 0, SHIP_SIZE, SHIP_SIZE //
                             2, 0, SHIP_SIZE, SHIP_SIZE, (255, 255, 255))
SHIP_MAX_SPEED = 10
SHIP_BULLETS = 50


class Ship(SpaceObject):
    """
    Class representing the player's ship.
    """

    def __init__(self, acceleration=.25, friction=.01, **kwargs):
        super().__init__(**kwargs, image=SHIP_IMAGE)
        self._acceleration = acceleration
        self._friction = friction
        self._bullets = SHIP_BULLETS

    @property
    def bullets_remaining(self):
        return self._bullets

    def thrust(self):
        """
        Accelerates the ship in the direction it is facing.
        """
        if self._velocity.length() < SHIP_MAX_SPEED:
            self._velocity += UP.rotate(self.angle) * self._acceleration

    def update(self, area=(INF, INF)):
        """
        Updates the ship's position, velocity, and direction.
        """
        self._velocity *= 1 - self._friction
        super().update(area)

    def fire(self):
        """
        Fires a bullet from the ship.

        Returns:
            Bullet: The bullet that was fired.
        """
        if self._bullets > 0:
            self._bullets -= 1
            return Bullet(
                position=self._position,
                velocity=self._velocity + UP.rotate(self.angle)*8,
                angle=self.angle,
            )
