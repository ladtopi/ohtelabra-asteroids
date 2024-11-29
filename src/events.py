import pygame


EVENT_SPAWN_SHIP = pygame.event.custom_type()
EVENT_SPAWN_ASTEROID_WAVE = pygame.event.custom_type()


class EventQueue:
    def post(self, event):
        pygame.event.post(event)

    def get(self):
        return pygame.event.get()

    def defer(self, event, delay_ms):
        pygame.time.set_timer(event, delay_ms, loops=1)
