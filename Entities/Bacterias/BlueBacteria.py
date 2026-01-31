from Entities.Bacterias.Bacteria import *
from Entities.Bacterias.RedBacteria import RedBacteria
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