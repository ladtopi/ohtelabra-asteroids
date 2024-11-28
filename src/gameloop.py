import pygame

from constants import EVENT_REPLACE_SHIP


class GameLoop:
    def __init__(self, state, renderer, event_queue, key_ctrl):
        self._state = state
        self._renderer = renderer
        self._event_queue = event_queue
        self._key_ctrl = key_ctrl

    def run(self):
        while True:
            if self._handle_events() == False:
                break
            self._state.update()
            self._renderer.render()

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == EVENT_REPLACE_SHIP:
                self._state.replace_ship()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._state.fire_ship()
                if event.key == pygame.K_RETURN and self._state.is_game_over():
                    self._state.reset()
                if event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:
                    # print("ctrl-r pressed")
                    # convenience feature for development
                    self._state.reset()

        pressed = self._key_ctrl.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            return False

        if pressed[pygame.K_UP]:
            self._state.thrust_ship()
        if pressed[pygame.K_RIGHT]:
            self._state.rotate_ship_right()
        if pressed[pygame.K_LEFT]:
            self._state.rotate_ship_left()

        return True
