"""Asteroid entity: procedural polygon, physics, split logic."""

import math
import random
import pygame
from .settings import WIDTH, HEIGHT, ASTEROID_SIZES, AST_COLOR, AST_OUTLINE
from .particle import ExplosionParticle


def _random_polygon(radius: int, n_verts: int) -> list[tuple[float, float]]:
  """Generate an irregular convex-ish polygon centred at origin."""
  angles = sorted(random.uniform(i * math.tau / n_verts,
                                 (i + 1) * math.tau / n_verts)
                  for i in range(n_verts))
  pts = []
  for a in angles:
    r = radius * random.uniform(0.72, 1.0)
    pts.append((math.cos(a) * r, math.sin(a) * r))
  return pts


class Asteroid:
  """A drifting asteroid with a randomised polygon shape."""

  def __init__(
    self,
    x: float, y: float,
    size: str = 'large',
    vx: float | None = None,
    vy: float | None = None,
    speed_mult: float = 1.0,
  ) -> None:
    self.size = size
    cfg = ASTEROID_SIZES[size]
    self.radius: int = cfg['radius']
    self.score: int = cfg['score']
    spd = cfg['speed'] * speed_mult

    self.x = x
    self.y = y
    angle = random.uniform(0, math.tau)
    self.vx = vx if vx is not None else math.cos(angle) * spd
    self.vy = vy if vy is not None else math.sin(angle) * spd
    self.spin = random.uniform(-1.2, 1.2)   # degrees/frame
    self.rotation = random.uniform(0, 360)

    self._base_pts = _random_polygon(self.radius, cfg['verts'])

  # ── Update ───────────────────────────────────────────────────────────────────
  def update(self) -> None:
    self.x = (self.x + self.vx) % WIDTH
    self.y = (self.y + self.vy) % HEIGHT
    self.rotation = (self.rotation + self.spin) % 360

  # ── Collision ─────────────────────────────────────────────────────────────────
  def collides_with_point(self, px: float, py: float, pr: float) -> bool:
    return math.hypot(px - self.x, py - self.y) < self.radius + pr

  # ── Split ─────────────────────────────────────────────────────────────────────
  def split(self, particles: list, speed_mult: float = 1.0) -> list['Asteroid']:
    """Destroy self and return child asteroids (if any)."""
    children: list[Asteroid] = []
    # Spawn explosion particles
    n_sparks = {'large': 25, 'medium': 15, 'small': 10}[self.size]
    for _ in range(n_sparks):
      particles.append(
        ExplosionParticle(self.x, self.y, big=(self.size == 'large'))
      )

    if self.size == 'large':
      next_size = 'medium'
    elif self.size == 'medium':
      next_size = 'small'
    else:
      return []   # small → just destroy

    for _ in range(2):
      offset_angle = random.uniform(0, math.tau)
      offset = self.radius * 0.5
      cx = self.x + math.cos(offset_angle) * offset
      cy = self.y + math.sin(offset_angle) * offset
      children.append(Asteroid(cx, cy, next_size, speed_mult=speed_mult))
    return children

  # ── Draw ─────────────────────────────────────────────────────────────────────
  def draw(self, surface: pygame.Surface) -> None:
    rad = math.radians(self.rotation)
    cos_r, sin_r = math.cos(rad), math.sin(rad)

    def rotate(pt: tuple[float, float]) -> tuple[int, int]:
      rx = pt[0] * cos_r - pt[1] * sin_r + self.x
      ry = pt[0] * sin_r + pt[1] * cos_r + self.y
      return (int(rx), int(ry))

    world_pts = [rotate(p) for p in self._base_pts]

    # Subtle fill
    fill_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(fill_surf, (*AST_COLOR, 40), world_pts)
    surface.blit(fill_surf, (0, 0))

    # Outline
    pygame.draw.polygon(surface, AST_OUTLINE, world_pts, 2)
