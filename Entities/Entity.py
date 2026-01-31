import random
from settings import *

class Entity:
    def __init__(self, x=None, y=None):
        if x is not None and y is not None:
            self.position_X = x
            self.position_Y = y
        else:
            self.position_X = random.uniform(0, WORLD_SIZE[0])
            self.position_Y = random.uniform(0, WORLD_SIZE[1])

    def get_screen_position(self, scale, offset):
        screen_x = int(self.position_X * scale) + int(offset[0])
        screen_y = int(self.position_Y * scale) + int(offset[1])
        return (screen_x, screen_y)