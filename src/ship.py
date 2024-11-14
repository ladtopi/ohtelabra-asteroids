import pygame

SHIP_W = 40
SHIP_H = 40
SHIP_IMAGE = pygame.Surface((SHIP_W, SHIP_H))
pygame.draw.polygon(SHIP_IMAGE, (255, 255, 255), ([0, SHIP_H],
                                                  [SHIP_W//2, 0],
                                                  [SHIP_W, SHIP_H]))


class Ship(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.angle = 0
        self.image = SHIP_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x-self.rect.width//2
        self.rect.y = y-self.rect.height//2
