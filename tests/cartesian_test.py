import unittest

from cartesian import contains, random_coords


class TestCartesian(unittest.TestCase):
    def test_contains_returns_true_if_area_contains_point(self):
        a = (0, 0, 10, 10)
        self.assertTrue(contains(a, (5, 5)))

    def test_contains_returns_false_for_non_overlapping_rectangles(self):
        a = (0, 0, 10, 10)
        self.assertFalse(contains(a, (12, 12)))

    def test_contains_treats_boundary_as_inclusive(self):
        a = (0, 0, 10, 10)
        self.assertTrue(contains(a, (0, 0)))
        self.assertTrue(contains(a, (10, 10)))

    def test_random_coords_returns_coordinates_in_area(self):
        area = (10, 10)
        for _ in range(1000):
            x, y = random_coords(area)
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x, 10)
            self.assertLessEqual(y, 10)

    def test_random_coords_does_not_return_coords_in_exclude_region(self):
        area = (20, 10)
        exclude_region = (0, 0, 10, 10)
        for _ in range(1000):
            x, _ = random_coords(area, exclude_region)
            self.assertGreaterEqual(x, 10)

    def test_random_coords_obeys_the_specified_margin(self):
        area = (30, 30)
        exclude_region = (5, 5, 10, 10)
        margin = 5
        # effectively, all points should land outside of the (0,0,20,20) region
        for _ in range(1000):
            x, y = random_coords(area, exclude_region, margin)
            self.assertTrue(x >= 20 or y >= 20)
