import pygame
from setting import *
from button import Button

pygame.init()

# Set the dimensions of the screen
screen = pygame.display.set_mode((screenwidth, screenheight))

clock = pygame.time.Clock()

#define the button    
start_button = Button(320,"Start",WHITE)
option_button = Button(420,"Option",WHITE)
help_button = Button(520,"Help",WHITE)
quit_button = Button(620,"Quit",WHITE)

game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get mouse position
            mouse_pos = pygame.mouse.get_pos()
            if start_button.is_clicked(mouse_pos):
                from main import *
            elif option_button.is_clicked(mouse_pos):
                from option import * 
            elif help_button.is_clicked(mouse_pos):
                from help import * 
            elif quit_button.is_clicked(mouse_pos):
                game_running = False

    screen.fill(BLACK)
    # Draw the button
    start_button.draw(screen)
    option_button.draw(screen)
    help_button.draw(screen)
    quit_button.draw(screen)
    
    # Update every second
    pygame.display.flip()
    # Update the display
    pygame.display.update()

    # Tick the clock to control the frame rate
    clock.tick(120)

# Quit Pygame
if pygame.display.get_surface() is not None:
    pygame.display.quit()
pygame.quit()
