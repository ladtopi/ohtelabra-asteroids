from collections import defaultdict
import os

import pygame

from graphics.colors import WHITE

pygame.font.init()

FONT_FILE = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "assets",
        "g7starforce.ttf"))


def __get_font(size):
    return pygame.font.Font(FONT_FILE, size)


FONTS = defaultdict(lambda: __get_font(18))
FONTS["sm"] = __get_font(16)
FONTS["md"] = __get_font(20)
FONTS["lg"] = __get_font(24)


def draw_text(screen, text, pos, size="sm", color=WHITE):
    text = FONTS[size].render(text.upper(), True, color)
    x, y = pos
    if x < 0:
        x = screen.get_width() + x - text.get_width()
    if y < 0:
        y = screen.get_height() + y - text.get_height()
    return screen.blit(text, (x, y))


def draw_text_below(screen, text, rect, margin=10, size=24, color=WHITE):
    x, y = rect.topleft
    y += rect.height + margin
    return draw_text(screen, text, (x, y), size, color)


def draw_centered(screen, surf, y=None):
    x = (screen.get_width() - surf.get_width()) // 2
    y = y or (screen.get_height() - surf.get_height()) // 2
    return screen.blit(surf, (x, y))


def draw_centered_text(screen, text, y=None, size="sm", color=WHITE):
    text = FONTS[size].render(text.upper(), True, color)
    return draw_centered(screen, text, y)


def draw_centered_text_below(screen, text, rect, margin=10, size=24, color=WHITE):
    top = rect.bottom + margin
    return draw_centered_text(screen, text, y=top, size=size, color=color)
