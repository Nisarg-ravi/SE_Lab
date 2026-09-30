"""
collision: figures out whether a falling object is within the basket.
"""

# Used only if the falling object doesn't expose a `radius` attribute.
# (Objects spawn at y=-14, which suggests a radius of about 14.)
DEFAULT_RADIUS = 14


def is_caught(basket_rect, obj):
    """Circle-vs-rectangle overlap test.

    The object is treated as a circle centred at (obj.x, obj.y). We find the
    point on the basket rect closest to that centre and check whether it is
    within one radius. This requires overlap on both axes, so an object at the
    top of the screen is no longer "caught" just because the basket is below it.
    """
    radius = getattr(obj, "radius", DEFAULT_RADIUS)

    closest_x = max(basket_rect.left, min(obj.x, basket_rect.right))
    closest_y = max(basket_rect.top, min(obj.y, basket_rect.bottom))

    dx = obj.x - closest_x
    dy = obj.y - closest_y
    return dx * dx + dy * dy <= radius * radius
