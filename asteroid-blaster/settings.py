# settings.py — Global constants for Asteroid Blaster

# Window
WIDTH  = 800
HEIGHT = 600
FPS    = 60
TITLE  = "Asteroid Blaster"

# Colors (Atari-style palette)
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
CYAN       = (0,   255, 255)
YELLOW     = (255, 255, 0)
RED        = (220, 50,  50)
ORANGE     = (255, 140, 0)
DARK_GRAY  = (20,  20,  35)
DIM_CYAN   = (0,   180, 200)

# Player
PLAYER_SPEED    = 5     # px per frame
SHOOT_COOLDOWN  = 18    # frames between shots

# Bullet
BULLET_SPEED    = 12    # px per frame (upward)
BULLET_W        = 3
BULLET_H        = 12

# Asteroid
ASTEROID_SPEED_MIN = 2
ASTEROID_SPEED_MAX = 4
ASTEROID_SIZE_MIN  = 22
ASTEROID_SIZE_MAX  = 48
SPAWN_RATE         = 55  # frames between spawns (lower = harder)
