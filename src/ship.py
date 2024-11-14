import pygame
import pygame.gfxdraw

SHIP_SIZE = 40
SHIP_IMAGE = pygame.Surface((SHIP_SIZE, SHIP_SIZE))
pygame.gfxdraw.filled_trigon(SHIP_IMAGE, 0, SHIP_SIZE, SHIP_SIZE //
                             2, 0, SHIP_SIZE, SHIP_SIZE, (255, 255, 255))


class Ship(pygame.sprite.Sprite):
    ROTATION_SPEED = 0.5

    def __init__(self, x=0, y=0):
        super().__init__()
        self.angle = 0
        self.image = SHIP_IMAGE.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x-self.rect.width//2
        self.rect.y = y-self.rect.height//2

    def rotate_right(self):
        if self.angle < Ship.ROTATION_SPEED:
            self.angle += 360
        self.angle -= Ship.ROTATION_SPEED
        self.image = pygame.transform.rotate(SHIP_IMAGE, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_left(self):
        if self.angle > 360 - Ship.ROTATION_SPEED:
            self.angle -= 360
        self.angle += Ship.ROTATION_SPEED
        self.image = pygame.transform.rotate(SHIP_IMAGE, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
