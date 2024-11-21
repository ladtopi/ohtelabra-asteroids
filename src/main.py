import pygame

from constants import Event
from state import GameOverState, PlayingState


def main():
    w = 800
    h = 600

    display = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pysteroids")
    pygame.init()

    state = PlayingState(display=display)

    running = True

    while running:
        if pygame.event.get(pygame.QUIT):
            running = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if pygame.event.get(Event.GAME_OVER):
            state = GameOverState(display=display)

        state.handle_events(pygame.event, pygame.key)
        state.update(pygame.event)
        state.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
