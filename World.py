from Bacteria import Bacteria
from Food import Food
from settings import WORLD_SIZE

class World:
    def __init__(self,start_count_food=100, start_count_bacteria=50,count_food_per_update=10):
        self.bacteria_population = [Bacteria() for _ in range(start_count_bacteria)]
        self.food_list = [Food() for _ in range(start_count_food)]
        self.count_food_per_update = count_food_per_update

    def _found_the_closest_food(self, bacteria):
        closest_food = None
        min_distance = float('inf')
        for food in self.food_list:
            distance = ((bacteria.position_X - food.position_X) ** 2 + (bacteria.position_Y - food.position_Y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_food = food
        return closest_food

    def _eat_food(self, bacteria):
        if bacteria.target_food is None:
            return
        if bacteria.check_collision(bacteria.target_food) and bacteria.target_food in self.food_list:
            self.food_list.remove(bacteria.target_food)
            bacteria.health += 10
            return

    def _kill_dead_bacteria(self):
        self.bacteria_population = [b for b in self.bacteria_population if b.health > 0]

    def update(self):
        self._kill_dead_bacteria()
        for b in self.bacteria_population:
            self._eat_food(b)
            target_food = self._found_the_closest_food(b)
            b.set_target_food(target_food)
        for b in self.bacteria_population:
            b.move()
        self.create_food()
    def create_food(self):
        for _ in range(self.count_food_per_update):
            self.food_list.append(Food())
    def draw(self, screen):
        for b in self.bacteria_population:
            b.draw(screen)
        for f in self.food_list:
            f.draw(screen)

