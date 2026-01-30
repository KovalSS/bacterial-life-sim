import random
from settings import *
import pygame
from Food import Food
import math
from Entity import Entity

class Bacteria(Entity):
    def __init__(self):
        super().__init__()
        self.target_food = None
        self.angel = random.uniform(0, 360)
        self.speed = random.uniform(0.5, 2)
        self.MAX_HEALTH = random.uniform(80, 120)
        self.health = self.MAX_HEALTH

    def set_target_food(self, target_food:Food):
        if target_food is not None:
            self.target_food = target_food
            dx = target_food.position_X - self.position_X
            dy = target_food.position_Y - self.position_Y
            self.angel = math.degrees(math.atan2(dy, dx))

    def move(self):
        self.health -= self.speed * 3
        self.position_X += math.cos(math.radians(self.angel)) * self.speed
        self.position_Y += math.sin(math.radians(self.angel)) * self.speed
        self.position_X = max(0, min(WORLD_SIZE[0], self.position_X))
        self.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y))

    def draw(self, screen, scale, offset):
        pos = self.get_screen_position(scale, offset)
        radius = max(3, int(5 * (scale / 10)))
        pygame.draw.circle(screen, (255, 0, 0), pos, radius)

    def check_collision(self, food:Food):
        distance = ((self.position_X - food.position_X) ** 2 + (self.position_Y - food.position_Y) ** 2) ** 0.5
        return distance < 1

    def heal(self, amount):
        self.health += amount
        self.health = min(self.MAX_HEALTH, 120)