import random
from settings import *
import pygame
from Entities.Food import Food
import math
from Entities.Entity import Entity

class Bacteria(Entity):

    def __init__(self, color,penalty_speed=None,
                 penalty_MAX_HEALTH=None,
                 speed=None, MAX_HEALTH = None,
                 dna=None,MITOSIS_RATE=None):
        super().__init__()
        self.penalty_speed = penalty_speed
        self.penalty_MAX_HEALTH = penalty_MAX_HEALTH
        self.target = None
        self.angle = random.uniform(0, 360)
        self.color = color
        self.speed = speed
        self.MAX_HEALTH = MAX_HEALTH
        self.health = self.MAX_HEALTH
        self.MITOSIS_RATE = MITOSIS_RATE
        if dna is None:
            self.dna = {}
        else:
            self.dna = dna
        self.age = 0
        self.MAX_AGE = random.uniform(*MAX_AGE)

    def update(self, world):
        if self.is_dead():
            return None

        self.age += 1

        if self.target is None or (hasattr(self.target, 'is_dead') and self.target.is_dead()) or (
                self.target not in world.food_list and self.target not in world.bacteria_population):
            self.target = self.think(world)

        self.move(world)

        child = None
        if self.target and self.check_collision(self.target):
            self.eat(self.target, world)
            self.target = None
            child = self.reproduce()


        return child

    def can_eat(self, other):
        return False

    def think(self, world):
        pass

    def find_target(self, world, search_configs):
        closest = None
        min_dist = float('inf')

        for grid, bias in search_configs:
            nearby = world.get_nearby_from_grid(self, grid)

            for entity in nearby:
                if hasattr(entity, 'is_dead') and entity.is_dead():
                    continue

                dx = self.position_X - entity.position_X
                dy = self.position_Y - entity.position_Y
                real_dist = (dx ** 2 + dy ** 2) ** 0.5

                perceived_dist = real_dist - bias

                if perceived_dist < min_dist:
                    min_dist = perceived_dist
                    closest = entity

        return closest

    def calculate_angle(self, world):
        if self.target:
            dx = self.target.position_X - self.position_X
            dy = self.target.position_Y - self.position_Y
            self.angle = math.degrees(math.atan2(dy, dx))

    def move(self, world):
        self.calculate_angle(world)
        health_factor = 0.6 + (0.4 * self.get_health_percentage())

        current_speed = self.speed * health_factor

        metabolic_cost = (current_speed * self.penalty_speed) + (self.MAX_HEALTH * self.penalty_MAX_HEALTH)
        self.health -= metabolic_cost

        step_distance = current_speed

        if self.target and hasattr(self.target, 'position_X'):
            dx = self.target.position_X - self.position_X
            dy = self.target.position_Y - self.position_Y
            dist_to_target = (dx ** 2 + dy ** 2) ** 0.5

            if dist_to_target < step_distance:
                self.position_X = self.target.position_X
                self.position_Y = self.target.position_Y
                return

        self.position_X += math.cos(math.radians(self.angle)) * step_distance
        self.position_Y += math.sin(math.radians(self.angle)) * step_distance

        self.position_X = max(0, min(WORLD_SIZE[0], self.position_X))
        self.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y))

    def draw(self, screen, scale, offset):
        pos = self.get_screen_position(scale, offset)
        radius = max(3, int(5 * (scale / 10)))
        pygame.draw.circle(screen, self.color, pos, radius)

    def check_collision(self, entity:Entity):
        distance = ((self.position_X - entity.position_X) ** 2 + (self.position_Y - entity.position_Y) ** 2) ** 0.5
        return distance < 1

    def heal(self, amount):
        self.health += amount
        self.health = min(self.health, self.MAX_HEALTH)

    def is_dead(self):
        return self.health <= 0 or self.age >= self.MAX_AGE

    def get_health_percentage(self):
        return self.health / self.MAX_HEALTH

    def reproduce(self,**kwargs):
        if self.get_health_percentage() > 0.5 and random.random() < self.MITOSIS_RATE:
            self.health /= 2
            child_dna = self.dna.copy()
            for key in child_dna:
                child_dna[key] *= random.uniform(0.8, 1.2)
            child_speed = self.speed * random.uniform(0.8, 1.2)
            child_MAX_HEALTH = self.MAX_HEALTH * random.uniform(0.8, 1.2)
            child = self.__class__(speed=child_speed, MAX_HEALTH=child_MAX_HEALTH,dna=child_dna,**kwargs)
            child.position_X = max(0, min(WORLD_SIZE[0], self.position_X + random.uniform(-1, 1)))
            child.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y + random.uniform(-1, 1)))
            return child
        return None




