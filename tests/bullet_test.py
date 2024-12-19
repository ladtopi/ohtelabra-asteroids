import unittest

from core.bullet import Bullet


class TestBullet(unittest.TestCase):
    def setUp(self):
        self.bullet = Bullet(ttl=2)

    def test_bullet_should_get_ttl_from_constructor(self):
        self.assertEqual(self.bullet.ttl, 2)

    def test_bullet_should_decrease_ttl_on_update(self):
        self.bullet.update()
        self.assertEqual(self.bullet.ttl, 1)

    def test_bullet_should_be_killed_once_ttl_reached(self):
        self.bullet.update()
        self.bullet.update()
        self.assertEqual(self.bullet.ttl, 0)
        self.assertFalse(self.bullet.alive())
