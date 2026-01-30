import random
from settings import *
import pygame
from Food import Food
import math
from Entity import Entity

class Bacteria(Entity):

    def __init__(self, color,penalty_speed=None, penalty_MAX_HEALTH=None,  speed=None, MAX_HEALTH = None, dna=None):
        super().__init__()
        self.penalty_speed = penalty_speed
        self.penalty_MAX_HEALTH = penalty_MAX_HEALTH
        self.target = None
        self.angle = random.uniform(0, 360)
        self.color = color
        self.speed = speed if speed is not None else random.uniform(0.5, 2)
        self.MAX_HEALTH = MAX_HEALTH if speed is not None else random.uniform(80, 120)
        self.health = self.MAX_HEALTH
        if dna is not None:
            self.dna = dna
        else:
            self.dna = {
                "fear": random.uniform(0, 10),
                "hunger": random.uniform(0, 10),
                "fear_radius": random.uniform(10, 50)
            }

    def can_eat(self, other):
        return False

    def think(self, world):
        return None

    def eat(self, target):
        if target:
            self.heal(20)

    def calculate_angle(self, world):
        if self.target:
            dx = self.target.position_X - self.position_X
            dy = self.target.position_Y - self.position_Y
            self.angle = math.degrees(math.atan2(dy, dx))

    def move(self, world):
        self.calculate_angle(world)
        metabolic_cost = (self.speed * self.penalty_speed) + (self.MAX_HEALTH * self.penalty_MAX_HEALTH)
        self.health -= metabolic_cost
        self.position_X += math.cos(math.radians(self.angle)) * self.speed
        self.position_Y += math.sin(math.radians(self.angle)) * self.speed
        self.position_X = max(0, min(WORLD_SIZE[0], self.position_X))
        self.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y))

    def draw(self, screen, scale, offset):
        pos = self.get_screen_position(scale, offset)
        radius = max(3, int(5 * (scale / 10)))
        pygame.draw.circle(screen, self.color, pos, radius)

    def check_collision(self, food:Food):
        distance = ((self.position_X - food.position_X) ** 2 + (self.position_Y - food.position_Y) ** 2) ** 0.5
        return distance < 1

    def heal(self, amount):
        self.health += amount
        self.health = min(self.health, self.MAX_HEALTH)

    def is_dead(self):
        return self.health <= 0

    def get_health_percentage(self):
        return self.health / self.MAX_HEALTH

    def reproduce(self):
        if self.get_health_percentage() >= 0.8:
            self.health /= 2
            child_dna = self.dna.copy()
            child_dna["fear"] *= random.uniform(0.8, 1.2)
            child_dna["hunger"] *= random.uniform(0.8, 1.2)
            child_dna["fear_radius"] *= random.uniform(0.8, 1.2)

            child_speed = self.speed * random.uniform(0.8, 1.2)
            child_MAX_HEALTH = self.MAX_HEALTH * random.uniform(0.8, 1.2)
            child = self.__class__(speed=child_speed, MAX_HEALTH=child_MAX_HEALTH,dna=child_dna)
            child.position_X = max(0, min(WORLD_SIZE[0], self.position_X + random.uniform(-1, 1)))
            child.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y + random.uniform(-1, 1)))
            return child
        return None

class BlueBacteria(Bacteria):
    def __init__(self, speed=None, MAX_HEALTH=None, dna=None, penalty_speed=None, penalty_MAX_HEALTH=None):
        if MAX_HEALTH is None:
            MAX_HEALTH = random.uniform(150, 250)
        if speed is None:
            speed = random.uniform(1, 2)
        super().__init__(color=(0, 0, 255),
                         penalty_speed = penalty_speed if penalty_speed is not None else 0.5,
                         penalty_MAX_HEALTH = penalty_MAX_HEALTH if penalty_MAX_HEALTH is not None else 0.001,
                         speed=speed, MAX_HEALTH=MAX_HEALTH, dna=dna)

    def calculate_angle(self, world):
        total_dx = 0
        total_dy = 0
        if self.target:
            food_dx = self.target.position_X - self.position_X
            food_dy = self.target.position_Y - self.position_Y
            strength = self.dna["hunger"]
            total_dx += food_dx * strength
            total_dy += food_dy * strength

        for b in world.bacteria_population:
            if isinstance(b, RedBacteria) and not b.is_dead():
                dist = ((self.position_X - b.position_X) ** 2 + (self.position_Y - b.position_Y) ** 2) ** 0.5

                if dist < self.dna["fear_radius"] and dist > 0:
                    run_dx = self.position_X - b.position_X
                    run_dy = self.position_Y - b.position_Y
                    strength = self.dna["fear"] / dist

                    total_dx += run_dx * strength
                    total_dy += run_dy * strength

        if total_dx != 0 or total_dy != 0:
            self.angle = math.degrees(math.atan2(total_dy, total_dx))

    def can_eat(self, other):
        return isinstance(other, Food)

    def think(self, world):
        closest = None
        min_dist = float('inf')
        for f in world.food_list:
            if self.can_eat(f):
                dist = ((self.position_X - f.position_X) ** 2 + (self.position_Y - f.position_Y) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    closest = f
        return closest

    def eat(self, target, world):
        if target in world.food_list:
            world.food_list.remove(target)
            self.heal(20)

class RedBacteria(Bacteria):
    def __init__(self, speed=None, MAX_HEALTH=None, dna=None, penalty_speed=None, penalty_MAX_HEALTH=None):
        if MAX_HEALTH is None:
            MAX_HEALTH = random.uniform(80, 100)
        if speed is None:
            speed = random.uniform(1.5, 3)
        super().__init__(
            color=(255, 0, 0),
            speed=speed,
            MAX_HEALTH=MAX_HEALTH,
            dna=dna,
            penalty_speed = penalty_speed if penalty_speed is not None else 0.3,
            penalty_MAX_HEALTH = penalty_MAX_HEALTH if penalty_MAX_HEALTH is not None else 0.01
        )

    def can_eat(self, other):
        is_bacteria = isinstance(other, Bacteria)
        is_not_my_family = type(self) != type(other)
        return is_bacteria and is_not_my_family and not other.is_dead()

    def think(self, world):
        closest = None
        min_dist = float('inf')

        for b in world.bacteria_population:
            if self.can_eat(b):
                dist = ((self.position_X - b.position_X) ** 2 + (self.position_Y - b.position_Y) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    closest = b
        return closest

    def eat(self, target, world):
        if not target.is_dead():
            target.health = -100
            self.heal(50)