WORLD_SIZE = (200, 200)
CELL_SIZE = 50
GRID_WIDTH = int(WORLD_SIZE[0] / CELL_SIZE)
GRID_HEIGHT = int(WORLD_SIZE[1] / CELL_SIZE)

START_COUNT_FOOD = 150
MAX_FOOD_COUNT = 500
COUNT_FOOD_PER_UPDATE = 50


START_COUNT_BlueBacteria = 30
START_COUNT_RedBacteria = 5
START_COUNT_VioletBacteria = 0


SPEED_BlueBacteria = (0.5, 1.5)
MAX_HEALTH_BlueBacteria = (100, 500)
PENALTY_SPEED_BlueBacteria = 0.1
PENALTY_MAX_HEALTH_BlueBacteria = 0.001

SPEED_RedBacteria = (1.5, 2.0)
MAX_HEALTH_RedBacteria = (100, 500)
PENALTY_SPEED_RedBacteria = 0.01
PENALTY_MAX_HEALTH_RedBacteria = 0.01

SPEED_VioletBacteria = (1.0, 1.5)
MAX_HEALTH_VioletBacteria = (100, 200)
PENALTY_SPEED_VioletBacteria = 0.6
PENALTY_MAX_HEALTH_VioletBacteria = 0.01
hunting_bias_VioletBacteria = 10
