
import pygame
from setting import *
pygame.init()

screen = pygame.display.set_mode((screenwidth, screenheight))

# Set up the game clock
clock = pygame.time.Clock()

game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

       
    screen.fill(BLUE)

    # Update every second
    pygame.display.flip()
    # Update the display
    pygame.display.update()

    # Tick the clock to control the frame rate
    clock.tick(120)

# Quit Pygame
pygame.quit()