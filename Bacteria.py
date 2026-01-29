import random
from settings import WORLD_SIZE
import pygame
class Bacteria:
    def __init__(self):
        self.position_X = random.uniform(0, WORLD_SIZE[0])
        self.position_Y = random.uniform(0, WORLD_SIZE[1])
    def move(self):
        self.position_X += random.uniform(-1, 1)
        self.position_Y += random.uniform(-1, 1)
        self.position_X = max(0, min(WORLD_SIZE[0], self.position_X))
        self.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y))
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.position_X * 10), int(self.position_Y * 10)), 5)