import pygame


class SpaceObject(pygame.sprite.Sprite):
    """
    A common base class for all objects that are moving around in the space.
    """

    def __init__(self,
                 x=0,
                 y=0,
                 display=None,
                 image=None,
                 velocity=pygame.Vector2(0, 0),
                 position=pygame.Vector2(0, 0),
                 acceleration=0.005,
                 friction=0,
                 angle=0):
        super().__init__()
        self.angle = angle
        self.velocity = velocity
        self.position = position
        self.image = image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x-self.rect.width//2
        self.rect.y = y-self.rect.height//2
        self.acceleration = acceleration
        self.friction = friction
        self.display = display

    def update(self):
        self.velocity *= (1-self.friction)
        self.position += self.velocity
        self.screen_wrap()
        self.rect.center = self.position

    def screen_wrap(self):
        w, h = self.rect.size
        scr_w, scr_h = self.display.get_size()
        if self.position.x + w//2 < 0:
            self.position.x = scr_w + w//2
        if self.position.x - w//2 > scr_w:
            self.position.x = -w//2
        if self.position.y + h//2 < 0:
            self.position.y = scr_h + h//2
        if self.position.y - h//2 > scr_h:
            self.position.y = -h//2
