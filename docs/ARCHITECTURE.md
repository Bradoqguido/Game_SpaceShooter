# 🏗️ Architecture — Space Shooter (Asteroids)

## Tech Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| Engine gráfica | Pygame 2.x |
| Síntese de áudio | NumPy (geração procedural) |
| Empacotamento | PyInstaller (distribuição) |

---

## Estrutura de Módulos

```
space_shooter/
├── main.py              # Bootstrap: pygame.init + Game loop
├── requirements.txt
└── src/
    ├── settings.py      # Constantes globais (cores, velocidades, telas)
    ├── game.py          # Máquina de estados: PLAYING | PAUSED | GAME_OVER
    ├── player.py        # Entidade nave (desenho vetorial, física, tiro)
    ├── asteroid.py      # Entidade asteroide (polígono procedural, split)
    ├── bullet.py        # Projétil laser (com trail)
    ├── particle.py      # Efeitos de partículas (thruster, explosão)
    ├── sound.py         # Geração de SFX via NumPy (sem arquivos externos)
    ├── hud.py           # Overlay: pontuação, vidas, nível
    └── menu.py          # Menus: Pause (ESC), Game Over
```

---

## Diagrama de Estado do Jogo

```
         ┌──────────┐
    ┌───►│  PLAYING  │◄────────┐
    │    └────┬─────┘         │
   ESC        │ vidas=0     Reiniciar
    │    ┌────▼─────┐    ┌────┴─────┐
    └────┤  PAUSED  │    │ GAME_OVER│
         └──────────┘    └──────────┘
```

---

## Fluxo de Entidades por Frame

```
Game.update()
  ├── Player.update()         ← entrada WASD + SPACE
  ├── Asteroid.update() ×N    ← drift + wrap
  ├── Bullet.update() ×N      ← movimento + lifetime
  ├── Particle.update() ×N    ← fade out
  └── collision_check()
        ├── bullet × asteroid → split + score + explosion
        └── player × asteroid → vida -1 + respawn

Game.draw()
  ├── draw_starfield()         ← estrelas estáticas procedurais
  ├── Particle.draw() ×N       ← camada de baixo
  ├── Asteroid.draw() ×N
  ├── Bullet.draw() ×N
  ├── Player.draw()
  └── HUD.draw()
```

---

## Física da Nave

- **Thrust**: velocidade acumulada na direção do ângulo atual (`W`)
- **Rotação**: ângulo += rotação_speed × dt (`A`/`D`)
- **Fricção**: `vel *= FRICTION` (0.99 por frame) — desaceleração natural
- **Wrap**: posição modulo (WIDTH, HEIGHT) — topologia toroidal

---

## Sistema de Partículas

| Tipo | Trigger | Cor | Vida |
|---|---|---|---|
| `ThrusterParticle` | W pressionado | Laranja → Amarelo | 15–25 frames |
| `ExplosionParticle` | Asteroide destruído | Branco → Laranja → Vermelho | 30–60 frames |
| `ShipExplosion` | Nave destruída | Ciano → Branco | 45–80 frames |

---

## Geração de Som (procedural)

```python
# Síntese laser "pew" — sem arquivos externos
t = linspace(0, 0.15s, samples)
freq_sweep = linspace(900Hz → 150Hz)
wave = sin(2π × freq_sweep × t) × exp(-t × 25)  # envelope de decaimento
→ int16 stereo → pygame.Sound
```

---

## Progressão de Níveis

| Nível | Asteroides | Modificador de velocidade |
|---|---|---|
| 1 | 4 | 1.0× |
| 2 | 6 | 1.1× |
| 3 | 8 | 1.2× |
| N | 4 + N×2 | 1 + N×0.05× |
