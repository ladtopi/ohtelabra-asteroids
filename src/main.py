import pygame
from asteroid import Asteroid
from ship import Ship


def main():
    w = 800
    h = 600

    display = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pysteroids")

    objects = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    ship = Ship(x=w/2, y=h/2, display=display)
    asteroid1 = Asteroid(x=100, y=100, vx=0.05, vy=0.25, display=display)
    asteroid2 = Asteroid(x=600, y=200, vx=-.12, vy=.1, display=display)
    objects.add(ship)
    objects.add(asteroid1)
    objects.add(asteroid2)
    objects.draw(display)
    pygame.init()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = ship.fire()
                objects.add(bullet)
                bullets.add(bullet)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            ship.rotate_right()
        if keys[pygame.K_LEFT]:
            ship.rotate_left()
        if keys[pygame.K_UP]:
            ship.thrust()

        for obj in objects:
            obj.update()

        display.fill((0, 0, 0))
        objects.draw(display)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
