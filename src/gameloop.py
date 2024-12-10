import pygame
from events import EVENT_SPAWN_SHIP, EVENT_SPAWN_ASTEROID_WAVE


class GameLoop:
    """
    The main game loop that handles events, updates the game state, and renders the game.
    """

    def __init__(self, state, renderer, event_queue, kbd):
        """
        Initializes the GameLoop with the given state, renderer, event queue, and keyboard handler.

        Args:
            state: The initial game state.
            renderer: The renderer responsible for drawing the game.
            event_queue: The event queue for handling events.
            kbd: The keyboard handler for handling key presses.
        """
        self._state = state
        self._renderer = renderer
        self._event_queue = event_queue
        self._kbd = kbd

    def run(self):
        """
        Runs the main game loop, handling events, updating the game state, and rendering the game.
        """
        while True:
            if not self._handle_events():
                break
            if not self._handle_keys():
                break
            self._state.update()
            self._renderer.render(self._state)

    def _handle_events(self):
        """
        Handles events from the event queue.

        Returns:
            bool: False if the game should exit, True otherwise.
        """
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == EVENT_SPAWN_SHIP:
                self._state.spawn_ship()
            if event.type == EVENT_SPAWN_ASTEROID_WAVE:
                self._state.spawn_asteroid_wave()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._state.fire_ship()
                if event.key == pygame.K_RETURN and self._state.is_game_over():
                    self._state.reset()
                if event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:
                    self._state.reset()
                if event.key == pygame.K_d and event.mod & pygame.KMOD_CTRL:
                    self._state.nuke_asteroids()

        return True

    def _handle_keys(self):
        """
        Handles continuous key presses.

        Returns:
            bool: False if the game should exit, True otherwise.
        """
        if self._kbd.is_pressed(pygame.K_ESCAPE):
            return False

        if self._kbd.is_pressed(pygame.K_UP):
            self._state.thrust_ship()
        if self._kbd.is_pressed(pygame.K_RIGHT):
            self._state.rotate_ship_right()
        if self._kbd.is_pressed(pygame.K_LEFT):
            self._state.rotate_ship_left()

        return True
