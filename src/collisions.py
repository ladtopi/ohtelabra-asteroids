import pygame


class CollisionChecker:
    def get_collision(self, sprite, group):
        return pygame.sprite.spritecollideany(sprite, group)
