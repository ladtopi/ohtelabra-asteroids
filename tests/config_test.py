import os
import unittest

from config import Config


class TestConfig(unittest.TestCase):
    def test_config_defaults(self):
        config = Config()
        self.assertEqual(config.window_width, 800)
        self.assertEqual(config.window_height, 600)
        self.assertEqual(config.initial_wave_size, 3)
        self.assertEqual(config.ship_max_speed, 400)
        self.assertEqual(config.ship_bullets, 50)

    def test_config_overrides(self):
        os.environ["WINDOW_WIDTH"] = "100"
        os.environ["WINDOW_HEIGHT"] = "200"
        os.environ["INITIAL_WAVE_SIZE"] = "4"
        os.environ["SHIP_MAX_SPEED"] = "20"
        os.environ["SHIP_BULLETS"] = "100"

        config = Config()

        self.assertEqual(config.window_width, 100)
        self.assertEqual(config.window_height, 200)
        self.assertEqual(config.initial_wave_size, 4)
        self.assertEqual(config.ship_max_speed, 20)
        self.assertEqual(config.ship_bullets, 100)
