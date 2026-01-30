from Bacteria import *
from Food import Food
from settings import WORLD_SIZE
import pygame
class World:
    def __init__(self,start_count_food=100, start_count_bacteria=10,percentage_red = 0.1,count_food_per_update=10):
        self.bacteria_population = []

        for _ in range(int(start_count_bacteria * (1 - percentage_red))):
            self.bacteria_population.append(BlueBacteria())
        for _ in range(int(start_count_bacteria * percentage_red)):
            self.bacteria_population.append(RedBacteria())

        self.food_list = [Food() for _ in range(start_count_food)]
        self.count_food_per_update = count_food_per_update

        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.history = []
        self.max_history_length = 300

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

        blues = sum(1 for b in self.bacteria_population if isinstance(b, BlueBacteria))
        reds = sum(1 for b in self.bacteria_population if isinstance(b, RedBacteria))
        foods = len(self.food_list)

        self.history.append((blues, reds, foods))

        if len(self.history) > self.max_history_length:
            self.history.pop(0)

    def create_food(self):
        for _ in range(self.count_food_per_update):
            self.food_list.append(Food())

    def draw(self, screen):
        screen_w, screen_h = screen.get_size()
        game_width = int(screen_w * 0.75)
        panel_width = screen_w - game_width
        margin = 20
        available_w = game_width - margin * 2
        available_h = screen_h - margin * 2

        scale = min(available_w / WORLD_SIZE[0], available_h / WORLD_SIZE[1])

        draw_w = WORLD_SIZE[0] * scale
        draw_h = WORLD_SIZE[1] * scale
        offset_x = (game_width - draw_w) / 2
        offset_y = (screen_h - draw_h) / 2
        offset = (offset_x, offset_y)

        pygame.draw.rect(screen, (50, 50, 50), (offset_x, offset_y, draw_w, draw_h), 2)
        for f in self.food_list:
            f.draw(screen, scale, offset)
        for b in self.bacteria_population:
            b.draw(screen, scale, offset)
        self.draw_stats_panel(screen, game_width, 0, panel_width, screen_h)

    def draw_stats_panel(self, screen, x, y, w, h):
        pygame.draw.rect(screen, (30, 30, 30), (x, y, w, h))
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, h), 2)

        if len(self.history) < 2:
            return
        graph_margin = 20
        graph_h = h // 2
        graph_w = w - graph_margin * 2
        graph_x = x + graph_margin
        graph_y = y + 50  # Відступ зверху

        # Малюємо рамку графіка
        pygame.draw.rect(screen, (0, 0, 0), (graph_x, graph_y, graph_w, graph_h))
        pygame.draw.rect(screen, (100, 100, 100), (graph_x, graph_y, graph_w, graph_h), 1)

        max_val = 0
        for data in self.history:
            max_val = max(max_val, data[0], data[1], data[2])
        max_val = max(max_val, 50)

        def get_points(data_index):
            points = []
            for i, data in enumerate(self.history):
                value = data[data_index]  # 0-Blue, 1-Red, 2-Food

                px = graph_x + (i / len(self.history)) * graph_w

                py = (graph_y + graph_h) - (value / max_val) * graph_h
                points.append((px, py))
            return points

        pygame.draw.lines(screen, (0, 150, 0), False, get_points(2), 2)
        pygame.draw.lines(screen, (50, 50, 255), False, get_points(0), 2)
        pygame.draw.lines(screen, (255, 50, 50), False, get_points(1), 2)
        curr_blue, curr_red, curr_food = self.history[-1]

        screen.blit(self.font.render(f"Food: {curr_food}", True, (0, 200, 0)), (graph_x, graph_y + graph_h + 10))
        screen.blit(self.font.render(f"Blue: {curr_blue}", True, (100, 100, 255)), (graph_x, graph_y + graph_h + 30))
        screen.blit(self.font.render(f"Red: {curr_red}", True, (255, 100, 100)), (graph_x, graph_y + graph_h + 50))


