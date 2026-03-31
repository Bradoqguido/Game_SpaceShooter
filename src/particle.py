"""Particle effects: thruster flame and explosion sparks."""

import math
import random
import pygame
from .settings import (
  THRUSTER_HOT, THRUSTER_WRM, EXP_HOT, EXP_WARM, EXP_COOL, SHIP_COLOR
)


class ThrusterParticle:
  """Small spark emitted from the ship engine while thrusting."""

  def __init__(self, x: float, y: float, angle: float) -> None:
    # Emit backward relative to ship heading
    spread = random.uniform(-20, 20)
    emit_angle = math.radians(angle + 180 + spread)
    speed = random.uniform(1.5, 4.5)
    self.x = x + math.cos(emit_angle) * 8
    self.y = y + math.sin(emit_angle) * 8
    self.vx = math.cos(emit_angle) * speed
    self.vy = math.sin(emit_angle) * speed
    self.lifetime = random.randint(10, 22)
    self.max_life = self.lifetime
    self.radius = random.uniform(1.5, 3.0)

  def update(self) -> None:
    self.x += self.vx
    self.y += self.vy
    self.vx *= 0.93
    self.vy *= 0.93
    self.lifetime -= 1

  def is_dead(self) -> bool:
    return self.lifetime <= 0

  def draw(self, surface: pygame.Surface) -> None:
    ratio = self.lifetime / self.max_life
    if ratio > 0.5:
      color = THRUSTER_HOT
    else:
      color = THRUSTER_WRM
    alpha = int(220 * ratio)
    r = max(1, int(self.radius * ratio))
    s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (*color, alpha), (r, r), r)
    surface.blit(s, (int(self.x) - r, int(self.y) - r))


class ExplosionParticle:
  """Spark emitted when an asteroid is destroyed."""

  def __init__(self, x: float, y: float, big: bool = False) -> None:
    angle = random.uniform(0, math.tau)
    speed = random.uniform(1.0, 6.5) * (1.8 if big else 1.0)
    self.x = x
    self.y = y
    self.vx = math.cos(angle) * speed
    self.vy = math.sin(angle) * speed
    self.lifetime = random.randint(25, 55)
    self.max_life = self.lifetime
    self.radius = random.uniform(1.5, 4.0) * (1.5 if big else 1.0)

  def update(self) -> None:
    self.x += self.vx
    self.y += self.vy
    self.vx *= 0.95
    self.vy *= 0.95
    self.lifetime -= 1

  def is_dead(self) -> bool:
    return self.lifetime <= 0

  def draw(self, surface: pygame.Surface) -> None:
    ratio = self.lifetime / self.max_life
    if ratio > 0.6:
      color = EXP_HOT
    elif ratio > 0.3:
      color = EXP_WARM
    else:
      color = EXP_COOL
    alpha = int(240 * ratio)
    r = max(1, int(self.radius * ratio))
    s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (*color, alpha), (r, r), r)
    surface.blit(s, (int(self.x) - r, int(self.y) - r))


class ShipExplosionParticle:
  """Larger cyan sparks when the player ship is destroyed."""

  def __init__(self, x: float, y: float) -> None:
    angle = random.uniform(0, math.tau)
    speed = random.uniform(0.5, 5.0)
    self.x = x
    self.y = y
    self.vx = math.cos(angle) * speed
    self.vy = math.sin(angle) * speed
    self.lifetime = random.randint(40, 80)
    self.max_life = self.lifetime
    self.radius = random.uniform(2.0, 5.0)

  def update(self) -> None:
    self.x += self.vx
    self.y += self.vy
    self.vx *= 0.97
    self.vy *= 0.97
    self.lifetime -= 1

  def is_dead(self) -> bool:
    return self.lifetime <= 0

  def draw(self, surface: pygame.Surface) -> None:
    ratio = self.lifetime / self.max_life
    alpha = int(255 * ratio)
    r = max(1, int(self.radius * ratio))
    s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (*SHIP_COLOR, alpha), (r, r), r)
    surface.blit(s, (int(self.x) - r, int(self.y) - r))
