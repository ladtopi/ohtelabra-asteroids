import pygame


def draw_centered(screen, surf, y=None):
    x = (screen.get_width() - surf.get_width()) // 2
    y = y or (screen.get_height() - surf.get_height()) // 2
    return screen.blit(surf, (x, y))


def draw_centered_text(screen, text, y=None, size=24, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    text = font.render(text, True, color)
    return draw_centered(screen, text, y)


def draw_centered_text_below(screen, text, rect, margin=10, size=24, color=(255, 255, 255)):
    top = rect.bottom + margin
    return draw_centered_text(screen, text, y=top, size=size, color=color)
