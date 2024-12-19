import unittest

from core import Asteroid


class TestAsteroid(unittest.TestCase):
    def setUp(self):
        self.asteroid = Asteroid()

    def test_exploding_creates_fragments(self):
        frags = self.asteroid.explode()
        self.assertGreater(len(frags), 0)

    def test_exploding_returns_no_frags_if_asteroid_already_of_smallest_size(self):
        self.asteroid = Asteroid(level=1)
        self.assertEqual(self.asteroid.explode(), [])
