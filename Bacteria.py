import random
from settings import *
import pygame
from Food import Food
import math
from Entity import Entity

class Bacteria(Entity):

    def __init__(self, color,penalty_speed=None,
                 penalty_MAX_HEALTH=None,
                 speed=None, MAX_HEALTH = None,
                 dna_blue=None):
        super().__init__()
        self.penalty_speed = penalty_speed
        self.penalty_MAX_HEALTH = penalty_MAX_HEALTH
        self.target = None
        self.angle = random.uniform(0, 360)
        self.color = color
        self.speed = speed
        self.MAX_HEALTH = MAX_HEALTH
        self.health = self.MAX_HEALTH
        self.dna_blue = dna_blue

    def update(self, world):
        if self.is_dead():
            return None

        if self.target is None or (hasattr(self.target, 'is_dead') and self.target.is_dead()) or (
                self.target not in world.food_list and self.target not in world.bacteria_population):
            self.target = self.think(world)

        child = None
        if self.target and self.check_collision(self.target):
            self.eat(self.target, world)
            self.target = None
            child = self.reproduce()
        self.move(world)

        return child

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

    def check_collision(self, entity:Entity):
        distance = ((self.position_X - entity.position_X) ** 2 + (self.position_Y - entity.position_Y) ** 2) ** 0.5
        return distance < 1

    def heal(self, amount):
        self.health += amount
        self.health = min(self.health, self.MAX_HEALTH)

    def is_dead(self):
        return self.health <= 0

    def get_health_percentage(self):
        return self.health / self.MAX_HEALTH

    def reproduce(self,**kwargs):
        if self.get_health_percentage() >= 0.8:
            self.health /= 2
            child_speed = self.speed * random.uniform(0.8, 1.2)
            child_MAX_HEALTH = self.MAX_HEALTH * random.uniform(0.8, 1.2)
            child = self.__class__(speed=child_speed, MAX_HEALTH=child_MAX_HEALTH,**kwargs)
            child.position_X = max(0, min(WORLD_SIZE[0], self.position_X + random.uniform(-1, 1)))
            child.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y + random.uniform(-1, 1)))
            return child
        return None

class BlueBacteria(Bacteria):
    def __init__(self, speed=None,
                 MAX_HEALTH=None,
                 dna_blue=None,
                 penalty_speed=None,
                 penalty_MAX_HEALTH=None):
        MAX_HEALTH = MAX_HEALTH if MAX_HEALTH is not None else random.uniform(*MAX_HEALTH_BlueBacteria)
        speed = speed if  speed is not None else random.uniform(*SPEED_BlueBacteria)
        if dna_blue is None:
            dna_blue = {
                "fear": random.uniform(0, 10),
                "hunger": random.uniform(0, 10),
                "fear_radius": random.uniform(10, 50)
            }
        super().__init__(color=(0, 0, 255),
                         penalty_speed = penalty_speed if penalty_speed is not None else PENALTY_SPEED_BlueBacteria,
                         penalty_MAX_HEALTH = penalty_MAX_HEALTH if penalty_MAX_HEALTH is not None else PENALTY_MAX_HEALTH_BlueBacteria,
                         speed=speed, MAX_HEALTH=MAX_HEALTH, dna_blue=dna_blue)

    def calculate_angle(self, world):
        total_dx = 0
        total_dy = 0
        if self.target:
            food_dx = self.target.position_X - self.position_X
            food_dy = self.target.position_Y - self.position_Y
            strength = self.dna_blue["hunger"]
            total_dx += food_dx * strength
            total_dy += food_dy * strength

        for b in world.bacteria_population:
            if isinstance(b, RedBacteria) and not b.is_dead():
                dist = ((self.position_X - b.position_X) ** 2 + (self.position_Y - b.position_Y) ** 2) ** 0.5

                if dist < self.dna_blue["fear_radius"] and dist > 0:
                    run_dx = self.position_X - b.position_X
                    run_dy = self.position_Y - b.position_Y
                    strength = self.dna_blue["fear"] / dist

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

    def reproduce(self):
        child_dna = self.dna_blue.copy()
        child_dna["fear"] *= random.uniform(0.8, 1.2)
        child_dna["hunger"] *= random.uniform(0.8, 1.2)
        child_dna["fear_radius"] *= random.uniform(0.8, 1.2)
        return super().reproduce(dna_blue=child_dna)


class RedBacteria(Bacteria):
    def __init__(self, speed=None,
                 MAX_HEALTH=None,
                 dna_blue=None,
                 penalty_speed=None,
                 penalty_MAX_HEALTH=None):
        MAX_HEALTH = MAX_HEALTH if MAX_HEALTH is not None else random.uniform(*MAX_HEALTH_RedBacteria)
        speed = speed if speed is not None else random.uniform(*SPEED_RedBacteria)
        super().__init__(color=(255, 0, 0),
                         penalty_speed=penalty_speed if penalty_speed is not None else PENALTY_SPEED_RedBacteria,
                         penalty_MAX_HEALTH=penalty_MAX_HEALTH if penalty_MAX_HEALTH is not None else PENALTY_MAX_HEALTH_RedBacteria,
                         speed=speed, MAX_HEALTH=MAX_HEALTH, dna_blue=dna_blue)

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