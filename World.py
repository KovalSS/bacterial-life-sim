from Bacteria import Bacteria
from Food import Food
from settings import WORLD_SIZE
import pygame
class World:
    def __init__(self,start_count_food=100, start_count_bacteria=1,count_food_per_update=10):
        self.bacteria_population = [Bacteria() for _ in range(start_count_bacteria)]
        self.food_list = [Food() for _ in range(start_count_food)]
        self.count_food_per_update = count_food_per_update

        self.font = pygame.font.SysFont("Arial", 20, bold=True)

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
            bacteria.heal(20)
            new_bacteria = bacteria.reproduce()
            if new_bacteria is not None:
                self.bacteria_population.append(new_bacteria)
            return

    def _kill_dead_bacteria(self):
        self.bacteria_population = [b for b in self.bacteria_population if not b.is_dead()]

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
        screen_w, screen_h = screen.get_size()

        margin = 40
        available_w = screen_w - margin * 2
        available_h = screen_h - margin * 2

        scale_x = available_w / WORLD_SIZE[0]
        scale_y = available_h / WORLD_SIZE[1]
        scale = min(scale_x, scale_y)


        draw_w = WORLD_SIZE[0] * scale
        draw_h = WORLD_SIZE[1] * scale
        offset_x = (screen_w - draw_w) / 2
        offset_y = (screen_h - draw_h) / 2
        offset = (offset_x, offset_y)


        rect_rect = (offset_x, offset_y, draw_w, draw_h)
        pygame.draw.rect(screen, (50, 50, 50), rect_rect, 2)

        for b in self.bacteria_population:
            b.draw(screen, scale, offset)
        for f in self.food_list:
            f.draw(screen, scale, offset)


        self.draw_ui(screen, screen_w, screen_h)

    def draw_ui(self, screen, w, h):
        text_color = (0, 0, 0)

        info_bact = self.font.render(f"Bacteria: {len(self.bacteria_population)}", True, text_color)
        screen.blit(info_bact, (20, 20))


        info_food = self.font.render(f"Food: {len(self.food_list)}", True, text_color)
        screen.blit(info_food, (20, 50))

