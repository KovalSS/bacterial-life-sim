from Bacteria import *
from Food import Food
from settings import WORLD_SIZE
import pygame
class World:
    def __init__(self,start_count_food=100, start_count_bacteria=10,count_food_per_update=10):
        self.bacteria_population = []

        for _ in range(start_count_bacteria // 2):
            self.bacteria_population.append(BlueBacteria())
        for _ in range(start_count_bacteria // 2):
            self.bacteria_population.append(RedBacteria())

        self.food_list = [Food() for _ in range(start_count_food)]
        self.count_food_per_update = count_food_per_update

        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def update(self):
        self.bacteria_population = [b for b in self.bacteria_population if not b.is_dead()]

        new_babies = []
        for b in self.bacteria_population:
            if b.target is None or (hasattr(b.target, 'is_dead') and b.target.is_dead()) or (
                b.target not in self.food_list and b.target not in self.bacteria_population):
                b.target = b.think(self)


            if b.target:
                dx = b.target.position_X - b.position_X
                dy = b.target.position_Y - b.position_Y
                b.angle = math.degrees(math.atan2(dy, dx))


            if b.target and b.check_collision(b.target):
                b.eat(b.target, self)
                b.target = None
                child = b.reproduce()
                if child:
                    new_babies.append(child)
            b.move()
        self.bacteria_population.extend(new_babies)
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

        blues = sum(1 for b in self.bacteria_population if isinstance(b, BlueBacteria))
        reds = sum(1 for b in self.bacteria_population if isinstance(b, RedBacteria))

        screen.blit(self.font.render(f"Blue: {blues}", True, (0, 0, 200)), (20, 20))
        screen.blit(self.font.render(f"Red: {reds}", True, (200, 0, 0)), (20, 50))
        screen.blit(self.font.render(f"Food: {len(self.food_list)}", True, (0, 100, 0)), (20, 80))


