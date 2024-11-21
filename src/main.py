import pygame
from asteroid import Asteroid
from ship import Ship


def main():
    W = 800
    H = 600

    display = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pysteroids")

    objects = pygame.sprite.Group()
    ship = Ship(W/2, H/2, display=display)
    asteroid1 = Asteroid(100, 100, pygame.Vector2(0.05, 0.25), display=display)
    asteroid2 = Asteroid(600, 200, pygame.Vector2(-.12, .1), display=display)
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            ship.rotate_right()
        if keys[pygame.K_LEFT]:
            ship.rotate_left()
        if keys[pygame.K_UP]:
            ship.thrust()

        ship.update()
        asteroid1.update()
        asteroid2.update()

        display.fill((0, 0, 0))
        objects.draw(display)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
