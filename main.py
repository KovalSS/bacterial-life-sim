import pygame
from World import *
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Bacteria Life Simulation")
clock = pygame.time.Clock()
running = True
paused = False
simulation_speed = 15
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

    screen.fill((240, 240, 240))

    if not paused:
        world.update()

    world.draw(screen)


    font = pygame.font.SysFont("Arial", 16, bold=True)
    speed_text = font.render(f"Speed: {simulation_speed} FPS (UP/DOWN)", True, (50, 50, 50))
    screen.blit(speed_text, (screen.get_width() - 200, 20))

    if paused:
        pause_text = font.render("PAUSED (Press SPACE)", True, (255, 0, 0))
        screen.blit(pause_text, (screen.get_width() / 2 - 60, screen.get_height() - 40))

    pygame.display.flip()
    clock.tick(simulation_speed)

pygame.quit()