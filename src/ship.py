import pygame
import pygame.gfxdraw

from bullet import Bullet
from space_object import SpaceObject

SHIP_SIZE = 40
SHIP_IMAGE = pygame.Surface((SHIP_SIZE, SHIP_SIZE), pygame.SRCALPHA)
pygame.gfxdraw.filled_trigon(SHIP_IMAGE, 0, SHIP_SIZE, SHIP_SIZE //
                             2, 0, SHIP_SIZE, SHIP_SIZE, (255, 255, 255))
SHIP_MAX_SPEED = 2
SHIP_BULLETS = 50


class Ship(SpaceObject):
    """
    Class representing the player's ship.
    """

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            image=SHIP_IMAGE,
            acceleration=0.002,
            friction=0.0005,
        )
        self.bullets_remaining = SHIP_BULLETS

    def thrust(self):
        """
        Accelerates the ship in the direction it is facing.
        """
        if self.velocity.length() < SHIP_MAX_SPEED:
            self.velocity += pygame.Vector2(
                0, (-self.acceleration)).rotate(self.angle)

    def fire(self):
        """
        Fires a bullet from the ship.

        Returns:
            Bullet: The bullet that was fired.
        """
        if self.bullets_remaining < 1:
            return
        v = pygame.Vector2(0, -1.25).rotate(self.angle)
        x, y = self.position
        self.bullets_remaining -= 1
        return Bullet(
            x=x,
            y=y,
            vx=self.velocity.x + v.x,
            vy=self.velocity.y + v.y,
            angle=self.angle,
            display=self.display,
        )
