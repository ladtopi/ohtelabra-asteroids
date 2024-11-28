import pygame

from gameloop import GameLoop
from state import GameState
from rendering import GameView


def main():
    w = 800
    h = 600

    display = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pysteroids")
    pygame.init()

    state = GameState(display)
    renderer = GameView(state, display, pygame.display.flip)
    loop = GameLoop(state, renderer, pygame.event, pygame.key)

    loop.run()

    pygame.quit()


if __name__ == "__main__":
    main()
