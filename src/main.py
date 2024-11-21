import pygame

from constants import Event
from state import GameState
from rendering import GameView


def main():
    w = 800
    h = 600

    display = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pysteroids")
    pygame.init()

    state = GameState(display)
    view = GameView(state, display)

    running = True

    while running:
        if pygame.event.get(pygame.QUIT):
            running = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if pygame.event.get(Event.START_NEW_GAME):
            state = GameState(display)
            view = GameView(state, display)

        state.handle_events(pygame.event, pygame.key)
        state.update()

        view.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
