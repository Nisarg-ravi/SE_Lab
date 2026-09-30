"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame

FPS = 60
BOOST_DURATION_FRAMES = 3 * FPS      # boost lasts about 3 seconds
BOOST_COOLDOWN_FRAMES = 2 * FPS      # wait after a boost ends before the next
BOOST_SPEED_MULTIPLIER = 2


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed                     # current speed; the engine reads this
        self.boosted_frames = 0                # frames of boost remaining
        self.cooldown_frames = 0               # frames until boost is ready again
        self.normal_speed = speed
        self.boost_speed = speed * BOOST_SPEED_MULTIPLIER

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )

    # --- speed boost -----------------------------------------------------

    @property
    def is_boosted(self):
        return self.boosted_frames > 0

    @property
    def boost_ready(self):
        return self.boosted_frames == 0 and self.cooldown_frames == 0

    @property
    def boost_fraction(self):
        """Fraction of the boost remaining, 1.0 (just started) to 0.0."""
        return self.boosted_frames / BOOST_DURATION_FRAMES

    @property
    def cooldown_seconds(self):
        return self.cooldown_frames / FPS

    def activate_boost(self):
        """Start a boost if one isn't active and the cooldown is over.
        Returns True if the boost started."""
        if not self.boost_ready:
            return False
        self.boosted_frames = BOOST_DURATION_FRAMES
        self.speed = self.boost_speed
        return True

    def update_boost(self):
        """Advance the boost/cooldown timers by one frame. Call once per frame."""
        if self.boosted_frames > 0:
            self.boosted_frames -= 1
            if self.boosted_frames == 0:
                self.speed = self.normal_speed
                self.cooldown_frames = BOOST_COOLDOWN_FRAMES
        elif self.cooldown_frames > 0:
            self.cooldown_frames -= 1
