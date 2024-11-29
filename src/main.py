import pygame

from collisions import CollisionChecker
from events import EventQueue
from gameloop import GameLoop
from keyboard import Keyboard
from state import GameState
from rendering import GameRenderer


def main():
    w = 800
    h = 600

    display = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pysteroids")
    pygame.init()

    collision_checker = CollisionChecker()
    event_queue = EventQueue()
    keyboard = Keyboard()
    state = GameState(collision_checker, event_queue, display).reset()
    renderer = GameRenderer(display, pygame.display.flip)
    loop = GameLoop(state, renderer, event_queue, keyboard)

    loop.run()

    pygame.quit()


if __name__ == "__main__":
    main()
