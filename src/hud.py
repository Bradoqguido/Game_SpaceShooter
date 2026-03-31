"""HUD: score, lives, level overlay."""

import math
import pygame
from .settings import WIDTH, HUD_COLOR, SHIP_COLOR, SHIP_GLOW


class HUD:
  """Renders the heads-up display."""

  def __init__(self) -> None:
    self._font_lg = pygame.font.SysFont('consolas', 28, bold=True)
    self._font_sm = pygame.font.SysFont('consolas', 18)
    self._level_flash: int = 0
    self._level_text: str = ''

  def show_level(self, level: int) -> None:
    """Trigger a level announcement banner."""
    self._level_text = f'LEVEL  {level}'
    self._level_flash = 120   # frames

  def update(self) -> None:
    if self._level_flash > 0:
      self._level_flash -= 1

  def draw(self, surface: pygame.Surface,
           score: int, lives: int, level: int, high_score: int) -> None:
    # Score
    score_surf = self._font_lg.render(f'{score:06d}', True, HUD_COLOR)
    surface.blit(score_surf, (16, 12))

    # High score label
    hs_surf = self._font_sm.render(f'BEST  {high_score:06d}', True,
                                   (*HUD_COLOR, 140))
    surface.blit(hs_surf, (16, 44))

    # Level (top centre)
    lv_surf = self._font_sm.render(f'LVL {level}', True, HUD_COLOR)
    surface.blit(lv_surf, (surface.get_width() // 2 - lv_surf.get_width() // 2, 14))

    # Lives (top right, drawn as tiny ship icons)
    self._draw_lives(surface, lives)

    # Level flash banner
    if self._level_flash > 0:
      alpha = min(255, self._level_flash * 4)
      banner = self._font_lg.render(self._level_text, True, SHIP_COLOR)
      banner.set_alpha(alpha)
      cx = surface.get_width() // 2 - banner.get_width() // 2
      cy = surface.get_height() // 2 - 60
      surface.blit(banner, (cx, cy))

  def _draw_lives(self, surface: pygame.Surface, lives: int) -> None:
    """Draw small ship icons in the top-right corner."""
    icon_size = 10
    margin = 14
    for i in range(lives):
      cx = surface.get_width() - margin - i * (icon_size * 2 + 6)
      cy = 22
      rad = math.radians(-90)
      pts = [
        (cx + math.cos(rad) * icon_size,
         cy + math.sin(rad) * icon_size),
        (cx + math.cos(rad + 2.4) * icon_size * 0.7,
         cy + math.sin(rad + 2.4) * icon_size * 0.7),
        (cx + math.cos(rad - 2.4) * icon_size * 0.7,
         cy + math.sin(rad - 2.4) * icon_size * 0.7),
      ]
      pygame.draw.polygon(surface, SHIP_COLOR, pts, 2)
