"""Laser bullet projectile."""

import math
import pygame
from .settings import WIDTH, HEIGHT, BULLET_SPEED, BULLET_LIFETIME, BULLET_COLOR, BULLET_GLOW


class Bullet:
  """A laser projectile fired by the player."""

  RADIUS = 4

  def __init__(self, x: float, y: float, angle: float) -> None:
    rad = math.radians(angle)
    self.x = x + math.cos(rad) * 18
    self.y = y + math.sin(rad) * 18
    self.vx = math.cos(rad) * BULLET_SPEED
    self.vy = math.sin(rad) * BULLET_SPEED
    self.lifetime = BULLET_LIFETIME
    # Trail history
    self._trail: list[tuple[float, float]] = []

  # ── Update ──────────────────────────────────────────────────────────────────
  def update(self) -> None:
    self._trail.append((self.x, self.y))
    if len(self._trail) > 6:
      self._trail.pop(0)
    self.x = (self.x + self.vx) % WIDTH
    self.y = (self.y + self.vy) % HEIGHT
    self.lifetime -= 1

  def is_dead(self) -> bool:
    return self.lifetime <= 0

  # ── Draw ─────────────────────────────────────────────────────────────────────
  def draw(self, surface: pygame.Surface) -> None:
    # Draw fading trail
    for i, (tx, ty) in enumerate(self._trail):
      ratio = (i + 1) / len(self._trail)
      alpha = int(120 * ratio)
      r = max(1, int(self.RADIUS * ratio * 0.7))
      s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
      pygame.draw.circle(s, (*BULLET_GLOW, alpha), (r, r), r)
      surface.blit(s, (int(tx) - r, int(ty) - r))

    # Outer glow
    glow_r = self.RADIUS + 3
    gs = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
    pygame.draw.circle(gs, (*BULLET_GLOW, 80), (glow_r, glow_r), glow_r)
    surface.blit(gs, (int(self.x) - glow_r, int(self.y) - glow_r))

    # Core dot
    pygame.draw.circle(surface, BULLET_COLOR,
                       (int(self.x), int(self.y)), self.RADIUS)
