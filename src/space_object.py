import pygame


class SpaceObject(pygame.sprite.Sprite):
    """
    A common base class for all objects that are moving around in the space.
    """

    def __init__(self,
                 x=0,
                 y=0,
                 screen_size=(800, 600),
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
