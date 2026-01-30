import random
from settings import *
import pygame
class Food:
    def __init__(self):
        self.position_X = random.uniform(0, WORLD_SIZE[0])
        self.position_Y = random.uniform(0, WORLD_SIZE[1])
    def draw(self, screen):
        pos = (int(self.position_X * SCALE) + OFFSET[0], int(self.position_Y * SCALE) + OFFSET[1])
        pygame.draw.circle(screen, (0, 255, 0), pos, 3)
    def __eq__(self, other):
        return self.position_X == other.position_X and self.position_Y == other.position_Y