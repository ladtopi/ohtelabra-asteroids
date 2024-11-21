import unittest

from bullet import Bullet
from ship import Ship


class DisplayStub:
    def get_size(self):
        return (800, 600)


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = Ship(x=400, y=300, display=DisplayStub())

    def test_rotate_right_rotates_one_degree_clockwise(self):
        self.ship.rotate_right()
        # by pygame angle conventions, rotating clockwise decreases the angle
        self.assertEqual(self.ship.angle, 359)

    def test_rotate_left_rotates_one_degree_counter_clockwise(self):
        self.ship.rotate_left()
        self.assertEqual(self.ship.angle, 1)

    def test_turning_around_twice_returns_to_original_angle(self):
        self.ship.rotate_right(180)
        self.ship.rotate_right(180)
        self.assertEqual(self.ship.angle, 0)

    def test_thrust_increases_velocity_in_direction_of_ship(self):
        self.ship.rotate_right(180)
        self.ship.thrust()
        self.assertEqual(self.ship.velocity.x, 0)
        self.assertGreater(self.ship.velocity.y, 0)

    def test_thrust_increases_velocity_by_acceleration(self):
        self.ship.rotate_right(180)
        self.ship.thrust()
        self.assertEqual(self.ship.velocity.y, self.ship.acceleration)

    def test_thrust_increases_velocity_by_constant_steps(self):
        self.ship.rotate_right(180)
        self.ship.thrust()
        self.ship.thrust()
        self.ship.thrust()
        self.assertEqual(self.ship.velocity.y, self.ship.acceleration * 3)

    def test_fire_creates_a_new_bullet(self):
        self.assertTrue(isinstance(self.ship.fire(), Bullet))

    def test_fire_shoots_bullet_in_direction_of_ship(self):
        bullet = self.ship.fire()
        self.assertEqual(bullet.velocity.angle_to((0, -1)), 0)
