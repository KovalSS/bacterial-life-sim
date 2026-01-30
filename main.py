import pygame
from World import *

pygame.init()


screen = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
pygame.display.set_caption("Bacteria Simulation + Graphs")

clock = pygame.time.Clock()
running = True
paused = False
simulation_speed = 60
world = World()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_UP:
                simulation_speed += 5
            if event.key == pygame.K_DOWN:
                simulation_speed = max(1, simulation_speed - 5)

    screen.fill((20, 20, 20))

    if not paused:
        world.update()

    world.draw(screen)

    font = pygame.font.SysFont("Arial", 16)
    speed_text = font.render(f"Speed: {simulation_speed} FPS", True, (200, 200, 200))
    screen.blit(speed_text, (10, 10))

    if paused:
        pause_text = font.render("PAUSED", True, (255, 0, 0))
        screen.blit(pause_text, (screen.get_width() / 2, 20))

    pygame.display.flip()
    clock.tick(simulation_speed)

pygame.quit()