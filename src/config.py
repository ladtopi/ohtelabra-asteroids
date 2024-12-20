import os


class Config:
    def __init__(self):
        self.window_width = int(os.environ.get("WINDOW_WIDTH", 800))
        self.window_height = int(os.environ.get("WINDOW_HEIGHT", 600))
        self.initial_wave_size = int(os.environ.get("INITIAL_WAVE_SIZE", 3))
        self.ship_max_speed = int(os.environ.get("SHIP_MAX_SPEED", 10))
        self.ship_bullets = int(os.environ.get("SHIP_BULLETS", 50))


config = Config()
