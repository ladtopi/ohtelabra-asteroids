import pygame

from gameloop import GameLoop


def main():
    w = 800
    h = 600

    pygame.init()
    pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pysteroids")

    loop = GameLoop()

    loop.run()

    pygame.quit()


if __name__ == "__main__":
    main()
