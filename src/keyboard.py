import pygame


class Keyboard:
    def is_pressed(self, key):
        return pygame.key.get_pressed()[key]
