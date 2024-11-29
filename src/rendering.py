import pygame


FONT_SYS_MONO = pygame.font.get_fonts()[0]


class GameRenderer:
    def __init__(self, display, frame_cb=None):
        self.display = display
        self.frame_cb = frame_cb

    def render(self, state):
        self.display.fill((0, 0, 0))
        state.objects.draw(self.display)
        self.render_lives(state)
        self.render_score(state)
        if state.is_game_over():
            self.render_game_over(state)
        self.frame_cb()

    def render_lives(self, state):
        font = pygame.font.SysFont(FONT_SYS_MONO, 24)
        text = font.render(
            f"Ships: {state.ships_remaining}", True, (255, 255, 255))
        self.display.blit(text, (10, 10))

    def render_score(self, state):
        font = pygame.font.SysFont(FONT_SYS_MONO, 24)
        text = font.render(
            f"Score: {state.score}", True, (255, 255, 255))
        self.display.blit(text, (self.display.get_width() -
                          10 - text.get_width(), 10))

    def render_game_over(self, state):
        font_lg = pygame.font.SysFont(FONT_SYS_MONO, 36)
        font_md = pygame.font.SysFont(FONT_SYS_MONO, 24)
        game_over_text = font_lg.render("Game Over", True, (255, 0, 0))
        continue_text = font_md.render(
            "Press ENTER to start a new game", True, (255, 255, 255))
        x = self.display.get_width() / 2 - game_over_text.get_width() / 2
        y = self.display.get_height() / 2 - game_over_text.get_height() / 2
        self.display.blit(game_over_text, (x, y))
        x = self.display.get_width() / 2 - continue_text.get_width() / 2
        y += game_over_text.get_height()
        self.display.blit(continue_text, (x, y))
