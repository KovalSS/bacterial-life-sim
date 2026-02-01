from Entities.Bacterias.Bacteria import *
class RedBacteria(Bacteria):
    def __init__(self, speed=None,
                 MAX_HEALTH=None,
                 dna=None,
                 penalty_speed=None,
                 penalty_MAX_HEALTH=None,
                 MITOSIS_RATE=None):
        MAX_HEALTH = MAX_HEALTH if MAX_HEALTH is not None else random.uniform(*MAX_HEALTH_RedBacteria)
        speed = speed if speed is not None else random.uniform(*SPEED_RedBacteria)
        super().__init__(color=(255, 0, 0),
                         penalty_speed=penalty_speed if penalty_speed is not None else PENALTY_SPEED_RedBacteria,
                         penalty_MAX_HEALTH=penalty_MAX_HEALTH if penalty_MAX_HEALTH is not None else PENALTY_MAX_HEALTH_RedBacteria,
                         speed=speed, MAX_HEALTH=MAX_HEALTH, dna=dna, MITOSIS_RATE=MITOSIS_RATE_RedBacteria)


    def eat(self, target, world):
        if not target.is_dead():
            target.health = -100
            self.heal(50)

    def think(self, world):
        targets = [
            (world.grid_blue, 0),
            (world.grid_violet, 0)
        ]
        return self.find_target(world, targets)