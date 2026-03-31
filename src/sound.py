"""Procedural laser sound — no external audio files needed."""

import numpy as np
import pygame
from .settings import SAMPLE_RATE


def generate_laser_sound() -> pygame.mixer.Sound:
  """Return a pygame.Sound containing a synthesised laser 'pew'."""
  duration = 0.14   # seconds
  n_samples = int(SAMPLE_RATE * duration)
  t = np.linspace(0, duration, n_samples, endpoint=False)

  # Frequency sweep: 900 Hz → 140 Hz  (descending "pew" pitch)
  freq = np.linspace(900, 140, n_samples)
  wave = np.sin(2.0 * np.pi * np.cumsum(freq) / SAMPLE_RATE)

  # Amplitude envelope: sharp attack, fast exponential decay
  envelope = np.exp(-t * 28)
  wave = (wave * envelope * 0.6).astype(np.float32)

  # Add a thin noise layer for crispness
  noise = np.random.uniform(-0.05, 0.05, n_samples).astype(np.float32)
  wave = np.clip(wave + noise, -1.0, 1.0)

  # Convert to int16 stereo
  pcm = (wave * 32767).astype(np.int16)
  stereo = np.column_stack([pcm, pcm])

  sound = pygame.sndarray.make_sound(np.ascontiguousarray(stereo))
  sound.set_volume(0.55)
  return sound
