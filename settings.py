WIDTH = 1600
HEIGHT = 900
FPS = 60
WORLD_WIDTH, WORLD_HEIGHT = 10240, 10240

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)
PURPLE = (128,0,128)
BACKGROUND_COLOR = (0,255,0)

from enum import Enum

class GameState(Enum):
    START_SCREEN = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4


ENEMY_TYPES = {
    "goblin": {
        "image": "assets/enemies/goblin.png",
        "hp": 50,
        "damage": 10,
        "xp": 5,
        "scale": 1.0,
        "speed": 2.0
    },
    "orc": {
        "image": "assets/enemies/orc.png",
        "hp": 100,
        "damage": 20,
        "xp": 10,
        "scale": 1.5,
        "speed": 1.5
    }
}

ENEMY_WAVES = [
    {
        "multi": 1,
        "hp": 100,
        "max_hp": 100,
        "damage": 5,
        "xp": 1,
        "duration": 30,  # 10 seconds
    },
    {
        "multi": 1,
        "hp": 200,
        "max_hp": 200,
        "damage": 10,
        "xp": 2,
        "duration": 45,  # 10 seconds
    },
    {
        "multi": 2,
        "hp": 300,
        "max_hp": 300,
        "damage": 20,
        "xp": 3,
        "duration": 60,  # 10 seconds
    },
    {
        "multi": 2,
        "hp": 400,
        "max_hp": 400,
        "damage": 25,
        "xp": 10,
        "duration": 60,  # 10 seconds
    },
    {
        "multi": 3,
        "hp": 500,
        "max_hp": 500,
        "damage": 40,
        "xp": 15,
        "duration": 60,  # 10 seconds
    },
    {
        "multi": 5,
        "hp": 500,
        "max_hp": 500,
        "damage": 50,
        "xp": 50,
        "duration": 120,  # 10 seconds
    },
]
