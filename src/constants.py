from enum import IntEnum, StrEnum

import pygame


class Event(IntEnum):
    """
    Enumeration of event types.
    """
    GAME_OVER = pygame.event.custom_type()
    """
    Custom event type for game over.
    """
    START_NEW_GAME = pygame.event.custom_type()
    """
    Custom event type for starting a new game.
    """
    REPLACE_SHIP = pygame.event.custom_type()
    """
    Custom event type for replacing the ship.
    """


class FontFamily(StrEnum):
    """
    Enumeration of font types.
    """
    SYS_MONO = pygame.font.get_fonts()[0]
    """
    Monospace font for rendering text.
    """
