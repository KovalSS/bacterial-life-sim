import pygame
from World import *
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

world = World()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))

    world.update()
    world.draw(screen)

    pygame.display.flip()
    clock.tick(10)
pygame.quit()