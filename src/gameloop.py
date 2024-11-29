import pygame

from events import EVENT_SPAWN_SHIP


class GameLoop:
    def __init__(self, state, renderer, event_queue, kbd):
        self._state = state
        self._renderer = renderer
        self._event_queue = event_queue
        self._kbd = kbd

    def run(self):
        while True:
            if not self._handle_events():
                break
            self._state.update()
            self._renderer.render()

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == EVENT_SPAWN_SHIP:
                self._state.spawn_ship()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._state.fire_ship()
                if event.key == pygame.K_RETURN and self._state.is_game_over():
                    self._state.reset()
                if event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:
                    # print("ctrl-r pressed")
                    # convenience feature for development
                    self._state.reset()

        if self._kbd.is_pressed(pygame.K_ESCAPE):
            return False

        if self._kbd.is_pressed(pygame.K_UP):
            self._state.thrust_ship()
        if self._kbd.is_pressed(pygame.K_RIGHT):
            self._state.rotate_ship_right()
        if self._kbd.is_pressed(pygame.K_LEFT):
            self._state.rotate_ship_left()

        return True
