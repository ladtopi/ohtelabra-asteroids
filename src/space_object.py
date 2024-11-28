import pygame

UP = pygame.Vector2(0, -1)


class SpaceObject(pygame.sprite.Sprite):
    """
    A common base class for all objects that are moving around in the space.
    """

    # This needs a lot of arguments so the pylint warning is disabled
    # pylint: disable=too-many-arguments
    def __init__(self,
                 x=0,
                 y=0,
                 vx=0,
                 vy=0,
                 acceleration=0,
                 friction=0,
                 angle=0,
                 image=None,
                 display=None):
        super().__init__()
        self.direction = UP.rotate(angle)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(vx, vy)
        self.image_original = image.copy()
        self.image = pygame.transform.rotate(image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = self.position.x-self.rect.width//2
        self.rect.y = self.position.y-self.rect.height//2
        self.acceleration = acceleration
        self.friction = friction
        self.display = display

    @property
    def angle(self):
        angle = round(UP.angle_to(self.direction))
        if angle < 0:
            return 360 + angle
        return angle

    def rotate_right(self, degrees=1):
        self.direction.rotate_ip(degrees)
        self.image = pygame.transform.rotate(self.image_original, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_left(self, degrees=1):
        self.direction.rotate_ip(-degrees)
        self.image = pygame.transform.rotate(self.image_original, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.velocity *= (1-self.friction)
        self.position += self.velocity
        self.screen_wrap()
        self.rect.center = self.position

    def screen_wrap(self):
        w, h = self.rect.size
        scr_w, scr_h = self.display.get_size()
        if self.position.x + w/2 < 0:
            self.position.x = scr_w + w//2
        if self.position.x - w/2 > scr_w:
            self.position.x = -w//2
        if self.position.y + h/2 < 0:
            self.position.y = scr_h + h//2
        if self.position.y - h/2 > scr_h:
            self.position.y = -h//2
