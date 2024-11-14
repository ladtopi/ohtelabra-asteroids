import unittest

from ship import Ship


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = Ship(400, 300, (800, 600))

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
