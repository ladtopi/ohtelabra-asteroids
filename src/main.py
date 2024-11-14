import pygame
from ship import Ship


def main():
    W = 800
    H = 600

    display = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pysteroids")

    objects = pygame.sprite.Group()
    ship = Ship(W/2, H/2)
    objects.add(ship)
    objects.draw(display)
    pygame.init()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        # display.fill((0,0,0))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
