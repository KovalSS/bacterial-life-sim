WORLD_SIZE = (100, 100)
CELL_SIZE = 50
GRID_WIDTH = int(WORLD_SIZE[0] / CELL_SIZE)
GRID_HEIGHT = int(WORLD_SIZE[1] / CELL_SIZE)

START_COUNT_FOOD = 50
MAX_FOOD_COUNT = 500
COUNT_FOOD_PER_UPDATE = 20


START_COUNT_BlueBacteria = 30
START_COUNT_RedBacteria = 5
START_COUNT_VioletBacteria = 0

MAX_AGE = (200, 1000)

SPEED_BlueBacteria = (0.1, 0.5)
MAX_HEALTH_BlueBacteria = (100, 500)
PENALTY_SPEED_BlueBacteria = 0.5
PENALTY_MAX_HEALTH_BlueBacteria = 0.0
MITOSIS_RATE_BlueBacteria = 0.1

SPEED_RedBacteria = (0.2, 0.7)
MAX_HEALTH_RedBacteria = (200, 500)
PENALTY_SPEED_RedBacteria = 0.5
PENALTY_MAX_HEALTH_RedBacteria = 0.0
MITOSIS_RATE_RedBacteria = 0.05

SPEED_VioletBacteria = (1.0, 1.5)
MAX_HEALTH_VioletBacteria = (100, 200)
PENALTY_SPEED_VioletBacteria = 0.6
PENALTY_MAX_HEALTH_VioletBacteria = 0.01
hunting_bias_VioletBacteria = 10
MITOSIS_RATE_VioletBacteria = 0.1