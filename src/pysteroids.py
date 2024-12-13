import pygame

from loop import GameLoop


class Pysteroids:
    def __init__(self, w=800, h=600):
        pygame.init()
        pygame.display.set_caption("Pysteroids")
        pygame.display.set_mode((w, h))

        self._loop = GameLoop()

    def run(self):
        self._loop.run()
