"""Main game loop and state machine (PLAYING | PAUSED | GAME_OVER)."""

from __future__ import annotations
import random
import math
import pygame
from .settings import (
  WIDTH, HEIGHT, FPS, DARK_BG, STAR_COLOR,
  ASTEROID_START_COUNT, PLAYER_LIVES,
)
from .player import Player
from .asteroid import Asteroid
from .bullet import Bullet
from .particle import ThrusterParticle, ExplosionParticle, ShipExplosionParticle
from .hud import HUD
from .menu import PauseMenu, GameOverMenu
from .sound import generate_laser_sound


# ── State constants ─────────────────────────────────────────────────────────────
_PLAYING   = 'playing'
_PAUSED    = 'paused'
_GAME_OVER = 'game_over'


class Game:
  """Owns the screen, clock, and all game entities."""

  def __init__(self, screen: pygame.Surface) -> None:
    self.screen = screen
    self.clock = pygame.time.Clock()

    # Pre-generate procedural star field
    self._stars = [
      (random.randint(0, WIDTH), random.randint(0, HEIGHT),
       random.uniform(0.4, 1.5))
      for _ in range(180)
    ]

    # Sounds
    laser_sound = generate_laser_sound()

    # Entities & state
    self._laser_sound = laser_sound
    self._reset()

  # ── Public entry point ────────────────────────────────────────────────────────
  def run(self) -> None:
    """Main game loop."""
    running = True
    while running:
      dt = self.clock.tick(FPS)
      events = pygame.event.get()
      for ev in events:
        if ev.type == pygame.QUIT:
          running = False
        running = self._handle_event(ev, running)

      self._update()
      self._draw()
      pygame.display.flip()

  # ── Reset / New wave ──────────────────────────────────────────────────────────
  def _reset(self) -> None:
    """Full game reset (new game)."""
    self._state = _PLAYING
    self._score: int = 0
    self._high_score: int = getattr(self, '_high_score', 0)
    self._lives: int = PLAYER_LIVES
    self._level: int = 1
    self._speed_mult: float = 1.0
    self._death_timer: int = 0   # delay before respawn

    self._player = Player(self._laser_sound)
    self._asteroids: list[Asteroid] = []
    self._bullets: list[Bullet] = []
    self._particles: list = []

    self._hud = HUD()
    self._pause_menu = PauseMenu()
    self._gameover_menu = GameOverMenu()

    self._spawn_wave(self._level)
    self._hud.show_level(self._level)

  def _spawn_wave(self, level: int) -> None:
    """Create the asteroids for a new wave."""
    count = ASTEROID_START_COUNT + (level - 1) * 2
    self._speed_mult = 1.0 + (level - 1) * 0.08
    for _ in range(count):
      # Spawn away from the player centre
      while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        if math.hypot(x - WIDTH / 2, y - HEIGHT / 2) > 160:
          break
      self._asteroids.append(Asteroid(x, y, 'large',
                                       speed_mult=self._speed_mult))

  # ── Event handling ─────────────────────────────────────────────────────────────
  def _handle_event(self, ev: pygame.event.Event, running: bool) -> bool:
    if self._state == _PLAYING:
      if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
        self._state = _PAUSED

    elif self._state == _PAUSED:
      result = self._pause_menu.handle_event(ev)
      if result == PauseMenu.RESTART:
        self._reset()
      elif result == PauseMenu.QUIT:
        return False
      elif result == 'resume':
        self._state = _PLAYING

    elif self._state == _GAME_OVER:
      result = self._gameover_menu.handle_event(ev)
      if result == GameOverMenu.RESTART:
        self._reset()
      elif result == GameOverMenu.QUIT:
        return False

    return running

  # ── Update ─────────────────────────────────────────────────────────────────────
  def _update(self) -> None:
    if self._state != _PLAYING:
      return

    keys = pygame.key.get_pressed()

    # Update HUD animations
    self._hud.update()

    # Player update (only when alive)
    if self._death_timer == 0:
      self._player.update(keys, self._particles, self._bullets)
    else:
      self._death_timer -= 1
      if self._death_timer == 0:
        if self._lives <= 0:
          self._state = _GAME_OVER
          self._high_score = max(self._high_score, self._score)
        else:
          self._player.reset()

    # Bullets
    for b in self._bullets[:]:
      b.update()
      if b.is_dead():
        self._bullets.remove(b)

    # Asteroids
    for a in self._asteroids[:]:
      a.update()

    # Particles
    for p in self._particles[:]:
      p.update()
      if p.is_dead():
        self._particles.remove(p)

    # Collision: bullets vs asteroids
    self._check_bullet_asteroid_collisions()

    # Collision: player vs asteroids
    if self._death_timer == 0 and not self._player.is_invincible():
      self._check_player_asteroid_collision()

    # Next wave?
    if not self._asteroids:
      self._level += 1
      self._spawn_wave(self._level)
      self._hud.show_level(self._level)

  def _check_bullet_asteroid_collisions(self) -> None:
    for b in self._bullets[:]:
      for a in self._asteroids[:]:
        if a.collides_with_point(b.x, b.y, b.RADIUS):
          self._bullets.remove(b)
          self._asteroids.remove(a)
          self._score += a.score
          children = a.split(self._particles, self._speed_mult)
          self._asteroids.extend(children)
          break

  def _check_player_asteroid_collision(self) -> None:
    for a in self._asteroids:
      if a.collides_with_point(self._player.x, self._player.y,
                                self._player.RADIUS):
        self._player.explode(self._particles)
        self._lives -= 1
        self._death_timer = 90   # 1.5s before respawn attempt

  # ── Draw ──────────────────────────────────────────────────────────────────────
  def _draw(self) -> None:
    self.screen.fill(DARK_BG)
    self._draw_stars()

    for p in self._particles:
      p.draw(self.screen)
    for a in self._asteroids:
      a.draw(self.screen)
    for b in self._bullets:
      b.draw(self.screen)

    if self._death_timer == 0:
      self._player.draw(self.screen)

    self._hud.draw(self.screen, self._score, self._lives,
                   self._level, self._high_score)

    if self._state == _PAUSED:
      self._pause_menu.draw(self.screen)
    elif self._state == _GAME_OVER:
      self._gameover_menu.draw(self.screen, self._score, self._high_score)

  def _draw_stars(self) -> None:
    for sx, sy, bright in self._stars:
      c = int(bright * 160)
      pygame.draw.circle(self.screen, (c, c, min(255, c + 40)),
                         (sx, sy), 1)
