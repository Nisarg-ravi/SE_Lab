"""
GameEngine: owns the basket and all falling objects.

Basket movement (Task 2), controlled spawning (Task 3) and the SPACE
speed boost (Task 4) are done, along with the Task 1 catch detection
fixes in game/collision.py and the catch-checking loop below.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_MIN_FRAMES = 30
SPAWN_INTERVAL_MAX_FRAMES = 70
OBJECT_RADIUS = 14          # matches FallingObject's default radius
MIN_SPAWN_X_GAP = 60        # min horizontal distance from the previous spawn
MAX_OBJECTS = 8             # max objects on screen at once
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _next_spawn_interval(self):
        return random.randint(SPAWN_INTERVAL_MIN_FRAMES, SPAWN_INTERVAL_MAX_FRAMES)

    def _pick_spawn_x(self):
        """Random x fully inside the screen, at least MIN_SPAWN_X_GAP away
        from the previous spawn x (when there was one)."""
        lo = OBJECT_RADIUS
        hi = WIDTH - OBJECT_RADIUS

        if self.last_spawn_x is None:
            return random.randint(lo, hi)

        # Allowed ranges on either side of the excluded zone around the last x.
        ranges = []
        left_hi = min(hi, int(self.last_spawn_x - MIN_SPAWN_X_GAP))
        if left_hi >= lo:
            ranges.append((lo, left_hi))
        right_lo = max(lo, int(self.last_spawn_x + MIN_SPAWN_X_GAP))
        if right_lo <= hi:
            ranges.append((right_lo, hi))

        if not ranges:  # screen too narrow to honour the gap; just stay on screen
            return random.randint(lo, hi)

        # Pick uniformly across the allowed pixels, not per range.
        total = sum(b - a + 1 for a, b in ranges)
        pick = random.randrange(total)
        for a, b in ranges:
            size = b - a + 1
            if pick < size:
                return a + pick
            pick -= size

    def _spawn_object(self):
        x = self._pick_spawn_x()
        self.last_spawn_x = x
        self.objects.append(
            FallingObject(x=x, y=-OBJECT_RADIUS, radius=OBJECT_RADIUS, speed=3)
        )

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        # Net direction: -1 (left), +1 (right), or 0 (neither, or both held).
        # Holding both keys cancels out cleanly instead of nudging the basket
        # one way and then the other within the same frame. The caller polls
        # keys_pressed every frame, so holding a key moves the basket a
        # constant `speed` pixels per frame with no key-repeat delay.
        direction = int(bool(keys_pressed[pygame.K_RIGHT])) - int(bool(keys_pressed[pygame.K_LEFT]))
        self.basket.x += direction * self.basket.speed

        # basket.x is the basket's centre, so keep it half a basket-width
        # away from each screen edge so the whole basket stays visible.
        half_width = self.basket.width / 2
        self.basket.x = max(half_width, min(WIDTH - half_width, self.basket.x))

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()
        elif not self.game_over and key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        self.basket.update_boost()

        # Spawn timer: counts down every frame. When it hits zero we spawn
        # only if we're under MAX_OBJECTS. At the cap the timer stays at zero,
        # so the next object appears as soon as there's room; otherwise the
        # timer is reset to a fresh random interval.
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0 and len(self.objects) < MAX_OBJECTS:
            self._spawn_object()
            self.frames_until_spawn = self._next_spawn_interval()

        for obj in self.objects:
            obj.update()

        # Catch detection: build a new list of survivors instead of removing
        # from self.objects while iterating over it, so nothing is skipped
        # and every caught object is credited exactly once.
        basket_rect = self.basket.get_rect()
        remaining = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                remaining.append(obj)
        self.objects = remaining

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))
        renderer.draw_boost_hud(surface, font, self.basket)

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")
