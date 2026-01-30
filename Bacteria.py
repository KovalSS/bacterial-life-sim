import random
from settings import *
import pygame
from Food import Food
import math
class Bacteria:
    def __init__(self):
        self.position_X = random.uniform(0, WORLD_SIZE[0])
        self.position_Y = random.uniform(0, WORLD_SIZE[1])
        self.target_food = None
        self.angel = random.uniform(0, 360)
        self.speed = random.uniform(0.5, 2)
        self.health = 100

    def set_target_food(self, target_food:Food):
        if target_food is not None:
            self.target_food = target_food
            dx = target_food.position_X - self.position_X
            dy = target_food.position_Y - self.position_Y
            self.angel = math.degrees(math.atan2(dy, dx))

    def move(self):
        self.health -= self.speed * 5
        self.position_X += math.cos(math.radians(self.angel)) * self.speed
        self.position_Y += math.sin(math.radians(self.angel)) * self.speed
        self.position_X = max(0, min(WORLD_SIZE[0], self.position_X))
        self.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y))

    def draw(self, screen):
        pos = (int(self.position_X * SCALE) + OFFSET[0], int(self.position_Y * SCALE) + OFFSET[1])
        pygame.draw.circle(screen, (255, 0, 0), pos, 5)

    def check_collision(self, food:Food):
        distance = ((self.position_X - food.position_X) ** 2 + (self.position_Y - food.position_Y) ** 2) ** 0.5
        return distance < 1