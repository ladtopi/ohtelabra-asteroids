import pygame

UP = pygame.Vector2(0, -1)
INF = float('inf')


class SpaceObject(pygame.sprite.Sprite):
    """
    A common base class for all objects that are moving around in the space.
    """

    # This needs a lot of arguments so the pylint warning is disabled
    # pylint: disable=too-many-arguments
    def __init__(self,
                 image: pygame.Surface,
                 size=None,
                 position=(0, 0),
                 velocity=(0, 0),
                 angle=0):
        super().__init__()
        self._direction = UP.rotate(angle)
        self._position = pygame.Vector2(*position)
        self._velocity = pygame.Vector2(*velocity)
        self._size = size or image.get_size()
        self._image_original = pygame.transform.scale(image, self._size)
        self._image = pygame.transform.rotate(image, -self.angle)
        self._rect = self.image.get_rect(center=self._position)

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    @property
    def x(self):
        return self._position.x

    @x.setter
    def x(self, value: int):
        self._position.x = value

    @property
    def y(self):
        return self._position.y

    @y.setter
    def y(self, value: int):
        self._position.y = value

    @property
    def w(self):
        return self.rect.width

    @property
    def h(self):
        return self.rect.height

    @property
    def vx(self):
        return self._velocity.x

    @property
    def vy(self):
        return self._velocity.y

    @property
    def angle(self):
        """
        Return the angle of the object in degrees.

        Returns:
            int: The angle of the object in degrees.
        """
        angle = round(UP.angle_to(self._direction))
        if angle < 0:
            angle += 360
        return angle

    @property
    def position(self):
        """
        Returns the position of the object as a tuple.

        Returns:
            (int, int): The position of the object as a tuple.
        """
        return self._position.x, self._position.y

    def rotate_right(self, degrees=1):
        """
        Rotate the object to the right, meaning clockwise.

        Args:
            degrees (int, optional): Degrees to turn. Defaults to 1.
        """
        self._direction.rotate_ip(degrees)
        self._image = pygame.transform.rotate(
            self._image_original, -self.angle)
        self._rect = self._image.get_rect(center=self._rect.center)

    def rotate_left(self, degrees=1):
        """
        Rotate the object to the left, meaning counterclockwise.

        Args:
            degrees (int, optional): Degrees to turn. Defaults to 1.
        """
        self._direction.rotate_ip(-degrees)
        self._image = pygame.transform.rotate(
            self._image_original, -self.angle)
        self._rect = self.image.get_rect(center=self.rect.center)

    def update(self, area=(INF, INF)):
        """
        Update the position of the object based on its velocity and acceleration.
        """
        self._position += self._velocity
        self._screen_wrap(area)
        self._rect.center = self._position

    def _screen_wrap(self, area: tuple[int, int]):
        if self.x < -self.w/2:
            self.x += area[0] + self.w/2
        if self.x > area[0] + self.w/2:
            self.x -= area[0] + self.w/2
        if self.y < -self.h/2:
            self.y += area[1] + self.h/2
        if self.y > area[1] + self.h/2:
            self.y -= area[1] + self.h/2
