import random
from settings import WORLD_SIZE
import pygame
class Food:
    def __init__(self):
        self.position_X = random.uniform(0, WORLD_SIZE[0])
        self.position_Y = random.uniform(0, WORLD_SIZE[1])
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.position_X * 10), int(self.position_Y * 10)), 3)