import pygame
import pygame.gfxdraw

ASTEROID_IMAGE = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.gfxdraw.filled_circle(ASTEROID_IMAGE, 20, 20, 19, (180, 220, 220))


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, v=pygame.Vector2(0, 0), screen_size=(800, 600)):
        super().__init__()
        self.velocity = v
        self.position = pygame.Vector2(x, y)
        self.image = ASTEROID_IMAGE.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x-self.rect.width//2
        self.rect.y = y-self.rect.height//2
        self.rotation_speed = 1
        self.acceleration = 0.005
        self.friction = 0
        self.screen_width, self.screen_height = screen_size

    def update(self):
        self.velocity *= (1-self.friction)
        self.position += self.velocity
        self.screen_wrap()
        self.rect.center = self.position

    def screen_wrap(self):
        if self.position.x + self.rect.width//2 < 0:
            self.position.x = self.screen_width + self.rect.width//2
        if self.position.x - self.rect.width//2 > self.screen_width:
            self.position.x = -self.rect.width//2
        if self.position.y + self.rect.height//2 < 0:
            self.position.y = self.screen_height + self.rect.height//2
        if self.position.y - self.rect.height//2 > self.screen_height:
            self.position.y = -self.rect.height//2
