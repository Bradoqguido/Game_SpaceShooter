"""Entry point for Space Shooter."""

import pygame
from src.settings import WIDTH, HEIGHT, TITLE, SAMPLE_RATE
from src.game import Game


def main() -> None:
  pygame.init()
  pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
  pygame.display.set_caption(TITLE)

  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption(TITLE)

  game = Game(screen)
  game.run()

  pygame.quit()


if __name__ == '__main__':
  main()
