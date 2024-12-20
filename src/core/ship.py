import pygame
import pygame.gfxdraw

from config import config
from core.bullet import Bullet
from core.space_object import INF, UP, SpaceObject
from graphics.colors import WHITE

SHIP_SIZE = 40
SHIP_IMAGE = pygame.Surface((SHIP_SIZE, SHIP_SIZE), pygame.SRCALPHA)
pygame.gfxdraw.filled_trigon(SHIP_IMAGE, 0, SHIP_SIZE, SHIP_SIZE //
                             2, 0, SHIP_SIZE, SHIP_SIZE, WHITE)


class Ship(SpaceObject):
    """
    Class representing the player's ship.
    """

    def __init__(
            self,
            acceleration=10,
            friction=0.25,
            max_speed=config.ship_max_speed,
            bullets=config.ship_bullets,
            immortal_for=0,
            **kwargs):
        super().__init__(**kwargs, image=SHIP_IMAGE)
        self._acceleration = acceleration
        self._friction = friction
        self._bullets = bullets
        self._max_speed = max_speed
        self._immortal_for = immortal_for

    @property
    def bullets_remaining(self):
        return self._bullets

    @property
    def immortal(self):
        return self._immortal_for > 0

    @property
    def mortal(self):
        return not self.immortal

    def make_immortal(self, seconds):
        self._immortal_for = seconds

    def thrust(self):
        """
        Accelerates the ship in the direction it is facing.
        """
        self._velocity += UP.rotate(self.angle) * self._acceleration
        self._velocity.scale_to_length(
            min(self._velocity.length(),
                self._max_speed))

    def update(self, area=(INF, INF), time_delta=1):
        """
        Updates the ship's position, velocity, and direction.
        """
        self._velocity *= (1 - self._friction) ** time_delta
        self._immortal_for = max(0, self._immortal_for - time_delta)
        super().update(area=area, time_delta=time_delta)
        self._blink()

    def _blink(self):
        """
        Blinks the ship to signal that it's immortal
        """
        if self.immortal:
            hundreds_of_ms = round(self._immortal_for * 1000, -2)
            self._image.set_alpha(255 if hundreds_of_ms % 400 == 0 else 100)

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
                velocity=self._velocity + UP.rotate(self.angle)*600,
                angle=self.angle,
            )
        return None
