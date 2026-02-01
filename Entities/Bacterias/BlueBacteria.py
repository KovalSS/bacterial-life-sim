from Entities.Bacterias.Bacteria import *
from Entities.Bacterias.FearMixin import FearMixin
class BlueBacteria(Bacteria, FearMixin):
    def __init__(self, speed=None,
                 MAX_HEALTH=None,
                 dna=None,
                 penalty_speed=None,
                 penalty_MAX_HEALTH=None,
                 MITOSIS_RATE=None):
        MAX_HEALTH = MAX_HEALTH if MAX_HEALTH is not None else random.uniform(*MAX_HEALTH_BlueBacteria)
        speed = speed if  speed is not None else random.uniform(*SPEED_BlueBacteria)
        if dna is None:
            dna = {
                "fear": random.uniform(*FEAR_BlueBacteria),
                "fear_radius": random.uniform(*FEAR_RADIUS_BlueBacteria)
            }
        super().__init__(color=(0, 0, 255),
                         penalty_speed = penalty_speed if penalty_speed is not None else PENALTY_SPEED_BlueBacteria,
                         penalty_MAX_HEALTH = penalty_MAX_HEALTH if penalty_MAX_HEALTH is not None else PENALTY_MAX_HEALTH_BlueBacteria,
                         speed=speed, MAX_HEALTH=MAX_HEALTH, dna=dna,MITOSIS_RATE=MITOSIS_RATE_BlueBacteria)

    def calculate_angle(self, world):
        total_dx = 0
        total_dy = 0
        if self.target:
            food_dx = self.target.position_X - self.position_X
            food_dy = self.target.position_Y - self.position_Y
            total_dx += food_dx
            total_dy += food_dy

        fear_dx, fear_dy = self.get_fear_vector(world, [world.grid_red, world.grid_violet])

        total_dx += fear_dx
        total_dy += fear_dy

        if total_dx != 0 or total_dy != 0:
            self.angle = math.degrees(math.atan2(total_dy, total_dx))

    def can_eat(self, other):
        return isinstance(other, Food)


    def eat(self, target, world):
        if target in world.food_list:
            world.food_list.remove(target)
            self.heal(20)

    def think(self, world):
        return self.find_target(world, [(world.grid_food, 0)])
