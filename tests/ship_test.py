import unittest

from core.bullet import Bullet
from core.ship import Ship


class DisplayStub:
    def get_size(self):
        return (800, 600)


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = Ship()

    def test_rotate_right_rotates_one_degree_clockwise(self):
        self.ship.rotate_right()
        self.assertEqual(self.ship.angle, 1)

    def test_rotate_left_rotates_one_degree_counter_clockwise(self):
        self.ship.rotate_left()
        self.assertEqual(self.ship.angle, 359)

    def test_turning_around_twice_returns_to_original_angle(self):
        self.ship.rotate_right(180)
        self.ship.rotate_right(180)
        self.assertEqual(self.ship.angle, 0)

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

    def test_fire_creates_a_new_bullet(self):
        self.assertTrue(isinstance(self.ship.fire(), Bullet))

    def test_fire_shoots_bullet_in_direction_of_ship(self):
        self.ship.rotate_right(33)
        bullet = self.ship.fire()
        self.assertAlmostEqual(bullet.angle, self.ship.angle)
