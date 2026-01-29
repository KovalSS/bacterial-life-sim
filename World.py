from Bacteria import Bacteria
from Food import Food
from settings import WORLD_SIZE

class World:
    def __init__(self,start_count_food=100, start_count_bacteria=50,count_food_per_update=10):
        self.bacteria_population = [Bacteria() for _ in range(start_count_bacteria)]
        self.food_list = [Food() for _ in range(start_count_food)]
        self.count_food_per_update = count_food_per_update
    def update(self):
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

