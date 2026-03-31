"""Pause and Game-Over menus."""

import pygame
from .settings import (
  WIDTH, HEIGHT,
  PAUSE_TITLE, MENU_SELECT, MENU_NORMAL, WHITE,
)


class _BaseMenu:
  """Shared rendering helpers."""

  def __init__(self, title: str, options: list[str]) -> None:
    self.title = title
    self.options = options
    self.selected: int = 0
    self._font_title = pygame.font.SysFont('consolas', 52, bold=True)
    self._font_opt   = pygame.font.SysFont('consolas', 30)
    self._font_hint  = pygame.font.SysFont('consolas', 16)

  # ── Input ────────────────────────────────────────────────────────────────────
  def handle_event(self, event: pygame.event.Event) -> str | None:
    """Return the chosen option name or None."""
    if event.type == pygame.KEYDOWN:
      if event.key in (pygame.K_UP, pygame.K_w):
        self.selected = (self.selected - 1) % len(self.options)
      elif event.key in (pygame.K_DOWN, pygame.K_s):
        self.selected = (self.selected + 1) % len(self.options)
      elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
        return self.options[self.selected]
    elif event.type == pygame.MOUSEBUTTONDOWN:
      for i, rect in enumerate(self._option_rects):
        if rect.collidepoint(event.pos):
          return self.options[i]
    elif event.type == pygame.MOUSEMOTION:
      for i, rect in enumerate(self._option_rects):
        if rect.collidepoint(event.pos):
          self.selected = i
    return None

  # ── Draw ─────────────────────────────────────────────────────────────────────
  def draw(self, surface: pygame.Surface) -> None:
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((4, 4, 20, 195))
    surface.blit(overlay, (0, 0))

    # Title
    title_surf = self._font_title.render(self.title, True, PAUSE_TITLE)
    title_surf.set_alpha(230)
    tx = WIDTH // 2 - title_surf.get_width() // 2
    surface.blit(title_surf, (tx, HEIGHT // 2 - 130))

    # Separator line
    pygame.draw.line(surface, (*PAUSE_TITLE, 100),
                     (WIDTH // 2 - 160, HEIGHT // 2 - 80),
                     (WIDTH // 2 + 160, HEIGHT // 2 - 80), 1)

    # Options
    self._option_rects: list[pygame.Rect] = []
    for i, opt in enumerate(self.options):
      color = MENU_SELECT if i == self.selected else MENU_NORMAL
      # Arrow indicator
      prefix = '▶  ' if i == self.selected else '   '
      surf = self._font_opt.render(prefix + opt, True, color)
      y = HEIGHT // 2 - 40 + i * 52
      x = WIDTH // 2 - surf.get_width() // 2
      rect = pygame.Rect(x, y, surf.get_width(), surf.get_height())
      self._option_rects.append(rect)
      surface.blit(surf, (x, y))

    # Hint
    hint = self._font_hint.render(
      'W/S ou ↑↓ para navegar  •  ENTER para confirmar', True, MENU_NORMAL)
    hint.set_alpha(120)
    surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 40))


class PauseMenu(_BaseMenu):
  """ESC pause overlay."""

  RESTART = 'Reiniciar'
  QUIT    = 'Sair'

  def __init__(self) -> None:
    super().__init__('PAUSADO', [self.RESTART, self.QUIT])

  def handle_event(self, event: pygame.event.Event) -> str | None:
    result = super().handle_event(event)
    # ESC also resumes
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      return 'resume'
    return result


class GameOverMenu(_BaseMenu):
  """Game-over screen."""

  RESTART = 'Jogar Novamente'
  QUIT    = 'Sair'

  def __init__(self) -> None:
    super().__init__('GAME  OVER', [self.RESTART, self.QUIT])

  def draw(self, surface: pygame.Surface,
           score: int = 0, high_score: int = 0) -> None:
    super().draw(surface)
    font = pygame.font.SysFont('consolas', 20)
    sc_surf = font.render(
      f'Pontuação: {score:06d}   |   Recorde: {high_score:06d}',
      True, WHITE)
    sc_surf.set_alpha(180)
    surface.blit(sc_surf,
                 (WIDTH // 2 - sc_surf.get_width() // 2, HEIGHT // 2 - 90))
