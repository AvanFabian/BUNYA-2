import pygame
from button import Button, Volume
from setting import *


pygame.init()

screen = pygame.display.set_mode((screenwidth, screenheight))


clock = pygame.time.Clock()


volume_button = Button(320,"Volume",WHITE)
back_button = Button(520,"Back",WHITE)
display_button = Button(420,"Display",WHITE)

music_volume = Volume(0.5, 0.0, 1.0, 0.1)
sfx_volume = Volume(0.7, 0.0, 1.0, 0.1)


game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get mouse position
            mouse_pos = pygame.mouse.get_pos()
            if volume_button.is_clicked(mouse_pos):
                print("Music volume:", music_volume.get_volume())
                print("SFX volume:", sfx_volume.get_volume())
                from volume import *  # assuming there's a run_volume function in volume
            elif display_button.is_clicked(mouse_pos):
                from display import *  # assuming there's a run_display function in display
            elif back_button.is_clicked(mouse_pos):
                from GUI import *
      
    screen.fill(BLACK)
    # Draw the button
    volume_button.draw(screen)
    display_button.draw(screen)
    back_button.draw(screen)
    
    # Update every second
    pygame.display.flip()
    # Update the display
    pygame.display.update()

    # Tick the clock to control the frame rate
    clock.tick(120)

# Quit Pygame
pygame.quit()
