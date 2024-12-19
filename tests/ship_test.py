import unittest

from core.bullet import Bullet
from core.ship import SHIP_MAX_SPEED, Ship


class DisplayStub:
    def get_size(self):
        return (800, 600)


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = Ship()

    def test_thrust_increases_velocity_in_direction_of_ship(self):
        self.ship = Ship(acceleration=1)
        self.ship.rotate_right(45)
        self.ship.thrust()
        self.assertGreater(abs(self.ship.vx), 0)
        self.assertGreater(abs(self.ship.vy), 0)

    def test_thrust_increases_velocity_by_acceleration(self):
        self.ship = Ship(acceleration=1)
        self.ship.rotate_right(180)
        self.ship.thrust()
        self.assertEqual(self.ship.vy, 1)

    def test_thrust_increases_velocity_by_constant_steps(self):
        self.ship = Ship(acceleration=.1)
        self.ship.rotate_right(180)
        self.ship.thrust()
        self.ship.thrust()
        self.ship.thrust()
        self.assertAlmostEqual(self.ship.vy, .3)

    def test_thrust_does_nothing_if_already_at_max_speed(self):
        self.ship = Ship(acceleration=1, velocity=(0, SHIP_MAX_SPEED))
        self.ship.rotate_right(180)
        self.ship.thrust()
        self.ship.thrust()
        self.ship.thrust()
        self.assertAlmostEqual(self.ship.speed, SHIP_MAX_SPEED)

    def test_fire_creates_a_new_bullet(self):
        self.assertTrue(isinstance(self.ship.fire(), Bullet))

    def test_fire_shoots_bullet_in_direction_of_ship(self):
        self.ship.rotate_right(33)
        bullet = self.ship.fire()
        self.assertAlmostEqual(bullet.angle, self.ship.angle)

    def test_fire_returns_none_if_no_bullets_remain(self):
        self.ship._bullets = 0
        self.assertIsNone(self.ship.fire())
