"""Player ship entity: drawing, physics, shooting."""

import math
import pygame
from .settings import (
  WIDTH, HEIGHT,
  PLAYER_THRUST, PLAYER_FRICTION, PLAYER_ROTATION_SPEED, PLAYER_MAX_SPEED,
  PLAYER_INVINCIBLE_TIME, BULLET_COOLDOWN,
  SHIP_COLOR, SHIP_GLOW,
)
from .bullet import Bullet
from .particle import ThrusterParticle, ShipExplosionParticle


class Player:
  """The player-controlled spaceship."""

  RADIUS = 16   # collision radius

  def __init__(self, laser_sound: pygame.mixer.Sound) -> None:
    self.laser_sound = laser_sound
    self.reset()

  # ── Lifecycle ────────────────────────────────────────────────────────────────
  def reset(self) -> None:
    """Respawn at screen centre."""
    self.x: float = WIDTH / 2
    self.y: float = HEIGHT / 2
    self.vx: float = 0.0
    self.vy: float = 0.0
    self.angle: float = -90.0   # pointing up
    self.invincible: int = PLAYER_INVINCIBLE_TIME
    self.bullet_timer: int = 0
    self.thrusting: bool = False

  def is_invincible(self) -> bool:
    return self.invincible > 0

  # ── Update ───────────────────────────────────────────────────────────────────
  def update(
    self,
    keys: pygame.key.ScancodeWrapper,
    particles: list,
    bullets: list,
  ) -> None:
    # Rotation (A / D)
    if keys[pygame.K_a]:
      self.angle -= PLAYER_ROTATION_SPEED
    if keys[pygame.K_d]:
      self.angle += PLAYER_ROTATION_SPEED

    # Thrust (W)
    self.thrusting = keys[pygame.K_w]
    if self.thrusting:
      rad = math.radians(self.angle)
      self.vx += math.cos(rad) * PLAYER_THRUST
      self.vy += math.sin(rad) * PLAYER_THRUST
      # Emit thruster particles
      for _ in range(2):
        particles.append(ThrusterParticle(self.x, self.y, self.angle))

    # Brake (S)
    if keys[pygame.K_s]:
      self.vx *= 0.92
      self.vy *= 0.92

    # Clamp speed
    speed = math.hypot(self.vx, self.vy)
    if speed > PLAYER_MAX_SPEED:
      scale = PLAYER_MAX_SPEED / speed
      self.vx *= scale
      self.vy *= scale

    # Friction
    self.vx *= PLAYER_FRICTION
    self.vy *= PLAYER_FRICTION

    # Move + wrap
    self.x = (self.x + self.vx) % WIDTH
    self.y = (self.y + self.vy) % HEIGHT

    # Invincibility countdown
    if self.invincible > 0:
      self.invincible -= 1

    # Bullet cooldown countdown
    if self.bullet_timer > 0:
      self.bullet_timer -= 1

    # Fire (SPACE)
    if keys[pygame.K_SPACE] and self.bullet_timer == 0:
      bullets.append(Bullet(self.x, self.y, self.angle))
      self.laser_sound.play()
      self.bullet_timer = BULLET_COOLDOWN

  def explode(self, particles: list) -> None:
    """Spawn destruction sparks."""
    for _ in range(40):
      particles.append(ShipExplosionParticle(self.x, self.y))

  # ── Draw ─────────────────────────────────────────────────────────────────────
  def _get_points(self) -> list[tuple[int, int]]:
    """Return the three vertices of the ship triangle in world coords."""
    rad = math.radians(self.angle)
    perp = math.radians(self.angle + 90)
    size = 16
    tip = (
      self.x + math.cos(rad) * size,
      self.y + math.sin(rad) * size,
    )
    left = (
      self.x + math.cos(perp) * size * 0.65 - math.cos(rad) * size * 0.7,
      self.y + math.sin(perp) * size * 0.65 - math.sin(rad) * size * 0.7,
    )
    right = (
      self.x - math.cos(perp) * size * 0.65 - math.cos(rad) * size * 0.7,
      self.y - math.sin(perp) * size * 0.65 - math.sin(rad) * size * 0.7,
    )
    return [tip, left, right]

  def draw(self, surface: pygame.Surface) -> None:
    # Blink when invincible
    if self.invincible > 0 and (self.invincible // 5) % 2 == 0:
      return

    pts = self._get_points()

    # Glow aura
    glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(glow_surf, (*SHIP_GLOW, 60), pts, 0)
    pygame.draw.polygon(glow_surf, (*SHIP_GLOW, 40), self._scaled_pts(1.35), 0)
    surface.blit(glow_surf, (0, 0))

    # Main hull
    pygame.draw.polygon(surface, SHIP_COLOR, pts, 2)

    # Engine exhaust line (always visible)
    rad = math.radians(self.angle)
    perp = math.radians(self.angle + 90)
    rear_x = self.x - math.cos(rad) * 10
    rear_y = self.y - math.sin(rad) * 10
    left_rear = (
      rear_x + math.cos(math.radians(self.angle + 90)) * 8,
      rear_y + math.sin(math.radians(self.angle + 90)) * 8,
    )
    right_rear = (
      rear_x - math.cos(math.radians(self.angle + 90)) * 8,
      rear_y - math.sin(math.radians(self.angle + 90)) * 8,
    )
    pygame.draw.line(surface, SHIP_GLOW, left_rear, right_rear, 2)

  def _scaled_pts(self, scale: float) -> list[tuple[float, float]]:
    rad = math.radians(self.angle)
    perp = math.radians(self.angle + 90)
    s = 16 * scale
    return [
      (self.x + math.cos(rad) * s,
       self.y + math.sin(rad) * s),
      (self.x + math.cos(perp) * s * 0.65 - math.cos(rad) * s * 0.7,
       self.y + math.sin(perp) * s * 0.65 - math.sin(rad) * s * 0.7),
      (self.x - math.cos(perp) * s * 0.65 - math.cos(rad) * s * 0.7,
       self.y - math.sin(perp) * s * 0.65 - math.sin(rad) * s * 0.7),
    ]
