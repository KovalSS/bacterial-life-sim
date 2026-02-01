from Entities.Bacterias.Bacteria import *
from Entities.Bacterias.RedBacteria import RedBacteria
from Entities.Bacterias.BlueBacteria import BlueBacteria
from Entities.Food import Food
class VioletBacteria(Bacteria):
    def __init__(self, speed=None,
                 MAX_HEALTH=None,
                 dna=None,
                 penalty_speed=None,
                 penalty_MAX_HEALTH=None,
                 MITOSIS_RATE=None):
        MAX_HEALTH = MAX_HEALTH if MAX_HEALTH is not None else random.uniform(*MAX_HEALTH_VioletBacteria)
        speed = speed if  speed is not None else random.uniform(*SPEED_VioletBacteria)
        if dna is None:
            dna = {
                "fear": random.uniform(0, 2),
                "fear_radius": random.uniform(10, 50)
            }
        super().__init__(color=(255, 0, 255),
                         penalty_speed = penalty_speed if penalty_speed is not None else PENALTY_SPEED_VioletBacteria,
                         penalty_MAX_HEALTH = penalty_MAX_HEALTH if penalty_MAX_HEALTH is not None else PENALTY_MAX_HEALTH_VioletBacteria,
                         speed=speed, MAX_HEALTH=MAX_HEALTH, dna=dna,MITOSIS_RATE=MITOSIS_RATE_VioletBacteria)

    def calculate_angle(self, world):
        total_dx = 0
        total_dy = 0
        if self.target:
            food_dx = self.target.position_X - self.position_X
            food_dy = self.target.position_Y - self.position_Y
            total_dx += food_dx
            total_dy += food_dy

        enemies = world.get_nearby_from_grid(self, world.grid_red)

        for enemy in enemies:
            if not enemy.is_dead():
                dist = ((self.position_X - enemy.position_X) ** 2 + (self.position_Y - enemy.position_Y) ** 2) ** 0.5

                if dist < self.dna["fear_radius"] and dist > 0:
                    run_dx = self.position_X - enemy.position_X
                    run_dy = self.position_Y - enemy.position_Y
                    strength = self.dna["fear"] / dist

                    total_dx += run_dx * strength
                    total_dy += run_dy * strength

        if total_dx != 0 or total_dy != 0:
            self.angle = math.degrees(math.atan2(total_dy, total_dx))

    def can_eat(self, other):
        return isinstance(other, Food) or isinstance(other, BlueBacteria)


    def eat(self, target, world):
        if target in world.food_list:
            world.food_list.remove(target)
            self.heal(20)
        elif isinstance(target, BlueBacteria) and not target.is_dead():
            target.health = -100
            self.heal(40)

    def think(self, world):
        targets = [
            (world.grid_food, 0),
            (world.grid_blue, 50)
        ]
        return self.find_target(world, targets)