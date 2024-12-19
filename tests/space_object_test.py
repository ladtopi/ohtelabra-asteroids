import unittest

import pygame

from core import SpaceObject


class TestSpaceObject(unittest.TestCase):
    def setUp(self):
        self.ob = SpaceObject(image=pygame.Surface((10, 10)))

    def test_rotate_right_rotates_one_degree_clockwise(self):
        self.ob.rotate_right()
        self.assertEqual(self.ob.angle, 1)

    def test_rotate_left_rotates_one_degree_counter_clockwise(self):
        self.ob.rotate_left()
        self.assertEqual(self.ob.angle, 359)

    def test_turning_around_twice_returns_to_original_angle(self):
        self.ob.rotate_right(180)
        self.ob.rotate_right(180)
        self.assertEqual(self.ob.angle, 0)

    def test_update_wraps_movement_horizontally(self):
        self.ob.x = 805
        self.ob.vx = 1
        self.ob.update((800, 100))
        self.assertEqual(self.ob.x, -4)
        self.ob.vx = -1
        self.ob.update((800, 100))
        self.assertEqual(self.ob.x, -5)
        self.ob.vx = -1
        self.ob.update((800, 100))
        self.assertEqual(self.ob.x, 804)

    def test_update_wraps_movement_vertically(self):
        self.ob.y = 805
        self.ob.vy = 1
        self.ob.update((100, 800))
        self.assertEqual(self.ob.y, -4)
        self.ob.vy = -1
        self.ob.update((100, 800))
        self.assertEqual(self.ob.y, -5)
        self.ob.vy = -1
        self.ob.update((100, 800))
        self.assertEqual(self.ob.y, 804)
