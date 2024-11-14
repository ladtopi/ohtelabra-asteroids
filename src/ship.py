import pygame
import pygame.gfxdraw

SHIP_SIZE = 40
SHIP_IMAGE = pygame.Surface((SHIP_SIZE, SHIP_SIZE), pygame.SRCALPHA)
pygame.gfxdraw.filled_trigon(SHIP_IMAGE, 0, SHIP_SIZE, SHIP_SIZE //
                             2, 0, SHIP_SIZE, SHIP_SIZE, (255, 255, 255))


class Ship(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, screen_size=(800, 600)):
        super().__init__()
        self.angle = 0
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(x, y)
        self.image = SHIP_IMAGE.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x-self.rect.width//2
        self.rect.y = y-self.rect.height//2
        self.acceleration = 0.002
        self.friction = 0.0005
        self.screen_width, self.screen_height = screen_size

    def rotate_right(self, degrees=1):
        if self.angle < degrees:
            self.angle += 360
        self.angle -= degrees
        self.image = pygame.transform.rotate(SHIP_IMAGE, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_left(self, degrees=1):
        if self.angle > 360 - degrees:
            self.angle -= 360
        self.angle += degrees
        self.image = pygame.transform.rotate(SHIP_IMAGE, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self):
        self.velocity += pygame.Vector2(
            0, (-self.acceleration)).rotate(-self.angle)

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
