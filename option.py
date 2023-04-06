import pygame
from setting import *
# import volume
# import display
from GUI import Button

pygame.init()

screen = pygame.display.set_mode((screenwidth, screenheight))

clock = pygame.time.Clock()

display_button = Button(420,"Display",WHITE)
volume_button = Button(320,"Volume",WHITE)
back_button = Button(520,"Back",WHITE)

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get mouse position
            mouse_pos = pygame.mouse.get_pos()
            if volume_button.is_clicked(mouse_pos):
                # volume.run_volume()  # assuming there's a run_volume function in volume
                print("volume clicked")
            elif display_button.is_clicked(mouse_pos):
                # display.run_display()  # assuming there's a run_display function in display
                print("display clicked")
            elif back_button.is_clicked(mouse_pos):
                print("back clicked")
      
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
