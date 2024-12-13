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
        self._position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(vx, vy)
        self.image_original = image.copy()
        self.image = pygame.transform.rotate(image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = self._position.x-self.rect.width//2
        self.rect.y = self._position.y-self.rect.height//2
        self.acceleration = acceleration
        self.friction = friction
        self.display = display

    @property
    def angle(self):
        """
        Return the angle of the object in degrees.

        Returns:
            int: The angle of the object in degrees.
        """
        angle = round(UP.angle_to(self.direction))
        if angle < 0:
            return 360 + angle
        return angle

    @property
    def position(self):
        """
        Returns the position of the object as a tuple.

        Returns:
            (int, int): The position of the object as a tuple.
        """
        return (self._position.x, self._position.y)

    def rotate_right(self, degrees=1):
        """
        Rotate the object to the right, meaning clockwise.

        Args:
            degrees (int, optional): Degrees to turn. Defaults to 1.
        """
        self.direction.rotate_ip(degrees)
        self.image = pygame.transform.rotate(self.image_original, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_left(self, degrees=1):
        """
        Rotate the object to the left, meaning counterclockwise.

        Args:
            degrees (int, optional): Degrees to turn. Defaults to 1.
        """
        self.direction.rotate_ip(-degrees)
        self.image = pygame.transform.rotate(self.image_original, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        """
        Update the position of the object based on its velocity and acceleration.
        """
        self.velocity *= (1-self.friction)
        self._position += self.velocity
        self._screen_wrap()
        self.rect.center = self._position

    def _screen_wrap(self):
        w, h = self.rect.size
        scr_w, scr_h = self.display.get_size()
        if self._position.x + w/2 < 0:
            self._position.x = scr_w + w//2
        if self._position.x - w/2 > scr_w:
            self._position.x = -w//2
        if self._position.y + h/2 < 0:
            self._position.y = scr_h + h//2
        if self._position.y - h/2 > scr_h:
            self._position.y = -h//2
