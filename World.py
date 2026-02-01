from Entities.Bacterias.RedBacteria import RedBacteria
from Entities.Bacterias.BlueBacteria import BlueBacteria
from Entities.Bacterias.VioletBacteria import VioletBacteria
from Entities.Food import Food
from settings import *
import pygame
class World:
    def __init__(self,start_count_food=START_COUNT_FOOD,
                 start_count_BlueBacteria=START_COUNT_BlueBacteria,
                 start_count_RedBacteria=START_COUNT_RedBacteria,
                 start_count_VioletBacteria=START_COUNT_VioletBacteria,
                 count_food_per_update=COUNT_FOOD_PER_UPDATE):
        self.grid_food = {}
        self.grid_blue = {}
        self.grid_red = {}
        self.grid_violet = {}
        self.bacteria_population = []

        for _ in range(start_count_BlueBacteria):
            self.bacteria_population.append(BlueBacteria())
        for _ in range(start_count_RedBacteria):
            self.bacteria_population.append(RedBacteria())
        for _ in range(start_count_VioletBacteria):
            self.bacteria_population.append(VioletBacteria())


        self.food_list = [Food() for _ in range(start_count_food)]
        self.count_food_per_update = count_food_per_update

        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.history = []
        self.max_history_length = 300

    def update_grid(self):
        self.grid_food = {}
        self.grid_blue = {}
        self.grid_red = {}
        self.grid_violet = {}

        for f in self.food_list:
            cx, cy = int(f.position_X // CELL_SIZE), int(f.position_Y // CELL_SIZE)
            if (cx, cy) not in self.grid_food: self.grid_food[(cx, cy)] = []
            self.grid_food[(cx, cy)].append(f)

        for b in self.bacteria_population:
            if b.is_dead(): continue

            cx, cy = int(b.position_X // CELL_SIZE), int(b.position_Y // CELL_SIZE)
            key = (cx, cy)

            b_type = type(b).__name__

            if b_type == "BlueBacteria":
                if key not in self.grid_blue: self.grid_blue[key] = []
                self.grid_blue[key].append(b)

            elif b_type == "RedBacteria":
                if key not in self.grid_red: self.grid_red[key] = []
                self.grid_red[key].append(b)

            elif b_type == "VioletBacteria":
                if key not in self.grid_violet: self.grid_violet[key] = []
                self.grid_violet[key].append(b)

    def get_nearby_from_grid(self, entity, target_grid):
        objects = []
        cx = int(entity.position_X // CELL_SIZE)
        cy = int(entity.position_Y // CELL_SIZE)

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                key = (cx + dx, cy + dy)
                if key in target_grid:
                    objects.extend(target_grid[key])
        return objects

    def check_repopulation(self):
        blues = sum(1 for b in self.bacteria_population if isinstance(b, BlueBacteria))
        reds = sum(1 for b in self.bacteria_population if isinstance(b, RedBacteria))

        if blues < MIN_BLUE_BACTERIA:
            for _ in range(RESPAWN_BLUE_AMOUNT):
                new_b = BlueBacteria()
                self.bacteria_population.append(new_b)

        if reds < MIN_RED_BACTERIA:
            for _ in range(RESPAWN_RED_AMOUNT):
                self.bacteria_population.append(RedBacteria())



    def update(self):
        self.check_repopulation()
        self.update_grid()
        self.bacteria_population = [b for b in self.bacteria_population if not b.is_dead()]
        new_babies = []

        for b in self.bacteria_population:
            child = b.update(self)
            if child:
                new_babies.append(child)

        self.bacteria_population.extend(new_babies)
        self.create_food()

        blues = sum(1 for b in self.bacteria_population if isinstance(b, BlueBacteria))
        reds = sum(1 for b in self.bacteria_population if isinstance(b, RedBacteria))
        violrs = sum(1 for b in self.bacteria_population if isinstance(b, VioletBacteria))
        foods = len(self.food_list)

        self.history.append((blues, reds,violrs, foods))

        if len(self.history) > self.max_history_length:
            self.history.pop(0)

    def create_food(self):
        if len(self.food_list) < MAX_FOOD_COUNT:
            for _ in range(self.count_food_per_update):
                 if len(self.food_list) < MAX_FOOD_COUNT:
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
        graph_y = y + 50

        # Малюємо рамку графіка
        pygame.draw.rect(screen, (0, 0, 0), (graph_x, graph_y, graph_w, graph_h))
        pygame.draw.rect(screen, (100, 100, 100), (graph_x, graph_y, graph_w, graph_h), 1)

        max_val = 0
        for data in self.history:
            max_val = max(max_val, data[0], data[1], data[2], data[3])
        max_val = max(max_val, 50)

        def get_points(data_index):
            points = []
            for i, data in enumerate(self.history):
                value = data[data_index]
                px = graph_x + (i / len(self.history)) * graph_w
                py = (graph_y + graph_h) - (value / max_val) * graph_h
                points.append((px, py))
            return points


        pygame.draw.lines(screen, (0, 150, 0), False, get_points(3), 2)
        pygame.draw.lines(screen, (50, 50, 255), False, get_points(0), 2)
        pygame.draw.lines(screen, (255, 50, 50), False, get_points(1), 2)
        pygame.draw.lines(screen, (255, 0, 255), False, get_points(2), 2)

        curr_blue, curr_red, curr_violet, curr_food = self.history[-1]

        screen.blit(self.font.render(f"Food: {curr_food}", True, (0, 200, 0)),
                    (graph_x, graph_y + graph_h + 10))
        screen.blit(self.font.render(f"Blue: {curr_blue}", True, (100, 100, 255)),
                    (graph_x, graph_y + graph_h + 30))
        screen.blit(self.font.render(f"Red: {curr_red}", True, (255, 100, 100)),
                    (graph_x, graph_y + graph_h + 50))
        screen.blit(self.font.render(f"Violet: {curr_violet}", True, (255, 0, 255)),
                    (graph_x, graph_y + graph_h + 70))


