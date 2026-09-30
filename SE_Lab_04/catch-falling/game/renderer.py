"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_BASKET_BOOST = (255, 200, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_BOOST_TEXT = (255, 220, 80)
COLOR_BOOST_READY = (120, 220, 140)
COLOR_BOOST_COOLDOWN = (170, 170, 180)
COLOR_BAR_BG = (60, 65, 85)

BOOST_BAR_SIZE = (140, 12)


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(surface, obj.color, (int(obj.x), int(obj.y)), obj.radius)
    color = COLOR_BASKET_BOOST if basket.is_boosted else COLOR_BASKET
    pygame.draw.rect(surface, color, basket.get_rect(), border_radius=6)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_boost_hud(surface, font, basket, pos=(10, 62)):
    """Boost status under the score/misses: an active "BOOST!" label with a
    remaining-time bar, or READY / cooldown text when not active."""
    x, y = pos
    if basket.is_boosted:
        draw_text(surface, font, "BOOST!", (x, y), COLOR_BOOST_TEXT)
        bar_w, bar_h = BOOST_BAR_SIZE
        bar_y = y + font.get_height() + 4
        pygame.draw.rect(surface, COLOR_BAR_BG, (x, bar_y, bar_w, bar_h), border_radius=4)
        fill_w = int(bar_w * basket.boost_fraction)
        if fill_w > 0:
            pygame.draw.rect(surface, COLOR_BASKET_BOOST, (x, bar_y, fill_w, bar_h), border_radius=4)
    elif basket.boost_ready:
        draw_text(surface, font, "Boost: READY (SPACE)", (x, y), COLOR_BOOST_READY)
    else:
        draw_text(
            surface, font,
            f"Boost: cooldown {basket.cooldown_seconds:.1f}s",
            (x, y), COLOR_BOOST_COOLDOWN,
        )


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)
