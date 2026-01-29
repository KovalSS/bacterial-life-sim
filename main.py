import pygame
import random
WORLD_SIZE = (128, 72)
class Bacteria:
    def __init__(self):
        self.position_X = random.uniform(0, WORLD_SIZE[0])
        self.position_Y = random.uniform(0, WORLD_SIZE[1])
    def move(self):
        self.position_X += random.uniform(-1, 1)
        self.position_Y += random.uniform(-1, 1)
        self.position_X = max(0, min(WORLD_SIZE[0], self.position_X))
        self.position_Y = max(0, min(WORLD_SIZE[1], self.position_Y))
    def draw(self):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.position_X * 10), int(self.position_Y * 10)), 5)



pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

population = [Bacteria() for _ in range(50)]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))

    for b in population:
        b.move()
        b.draw()

    pygame.display.flip()
    clock.tick(10)
pygame.quit()