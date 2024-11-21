import pygame

from constants import FontFamily


class GameView:
    def __init__(self, state, display):
        self.state = state
        self.display = display

    def render(self):
        self.display.fill((0, 0, 0))
        self.state.objects.draw(self.display)
        self.render_lives()
        self.render_score()
        if self.state.is_game_over():
            self.render_game_over()

    def render_lives(self):
        font = pygame.font.SysFont(FontFamily.SYS_MONO, 24)
        text = font.render(
            f"Ships: {self.state.ships_remaining}", True, (255, 255, 255))
        self.display.blit(text, (10, 10))

    def render_score(self):
        font = pygame.font.SysFont(FontFamily.SYS_MONO, 24)
        text = font.render(
            f"Score: {self.state.score}", True, (255, 255, 255))
        self.display.blit(text, (self.display.get_width() -
                          10 - text.get_width(), 10))

    def render_game_over(self):
        font_lg = pygame.font.SysFont(FontFamily.SYS_MONO, 36)
        font_md = pygame.font.SysFont(FontFamily.SYS_MONO, 24)
        game_over_text = font_lg.render("Game Over", True, (255, 0, 0))
        continue_text = font_md.render(
            "Press ENTER to start a new game", True, (255, 255, 255))
        x = self.display.get_width() / 2 - game_over_text.get_width() / 2
        y = self.display.get_height() / 2 - game_over_text.get_height() / 2
        self.display.blit(game_over_text, (x, y))
        x = self.display.get_width() / 2 - continue_text.get_width() / 2
        y += game_over_text.get_height()
        self.display.blit(continue_text, (x, y))