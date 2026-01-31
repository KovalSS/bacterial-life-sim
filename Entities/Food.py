import pygame
from Entities.Entity import Entity
class Food(Entity):
    def __init__(self):
        super().__init__()
    def draw(self, screen, scale, offset):
        pos = self.get_screen_position(scale, offset)
        radius = max(2, int(3 * (scale / 10)))
        pygame.draw.circle(screen, (0, 255, 0), pos, radius)
    def __eq__(self, other):
        return self.position_X == other.position_X and self.position_Y == other.position_Y