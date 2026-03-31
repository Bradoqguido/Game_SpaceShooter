"""Global constants for Space Shooter."""

# ── Screen ──────────────────────────────────────────────────────────────────
WIDTH  = 900
HEIGHT = 700
FPS    = 60
TITLE  = "Space Shooter — Asteroids"

# ── Colors ───────────────────────────────────────────────────────────────────
BLACK        = (0,   0,   0)
WHITE        = (255, 255, 255)
DARK_BG      = (5,   5,   20)
STAR_COLOR   = (180, 180, 220)
SHIP_COLOR   = (100, 210, 255)
SHIP_GLOW    = (40,  120, 255)
THRUSTER_HOT = (255, 200, 60)
THRUSTER_WRM = (255, 100, 20)
BULLET_COLOR = (0,   255, 210)
BULLET_GLOW  = (0,   160, 255)
AST_COLOR    = (170, 155, 125)
AST_OUTLINE  = (220, 200, 160)
EXP_HOT      = (255, 240, 100)
EXP_WARM     = (255, 130, 30)
EXP_COOL     = (200,  60,  30)
HUD_COLOR    = (160, 220, 255)
MENU_OVERLAY = (0,   0,   30, 180)
PAUSE_TITLE  = (100, 210, 255)
MENU_SELECT  = (0,   255, 180)
MENU_NORMAL  = (160, 180, 200)

# ── Player ────────────────────────────────────────────────────────────────────
PLAYER_THRUST          = 0.28
PLAYER_FRICTION        = 0.985
PLAYER_ROTATION_SPEED  = 3.8   # degrees/frame
PLAYER_MAX_SPEED       = 7.0
PLAYER_LIVES           = 3
PLAYER_INVINCIBLE_TIME = 180   # frames (~3s)
BULLET_COOLDOWN        = 18    # frames

# ── Bullet ────────────────────────────────────────────────────────────────────
BULLET_SPEED    = 13
BULLET_LIFETIME = 55   # frames

# ── Asteroids ─────────────────────────────────────────────────────────────────
ASTEROID_SIZES = {
  'large':  {'radius': 55, 'speed': 1.4, 'score': 20,  'verts': 11},
  'medium': {'radius': 30, 'speed': 2.3, 'score': 50,  'verts': 9},
  'small':  {'radius': 14, 'speed': 3.8, 'score': 100, 'verts': 7},
}
ASTEROID_START_COUNT = 4

# ── Sound ─────────────────────────────────────────────────────────────────────
SAMPLE_RATE = 44100
