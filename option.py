import pygame
from button import Button
from setting import *
import volume
import display

class Option:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((screenwidth, screenheight))
        self.clock = pygame.time.Clock()

        self.volume_button = Button(320, "Volume", WHITE)
        self.back_button = Button(520, "Back", WHITE)
        self.display_button = Button(420, "Display", WHITE)

        self.music_volume = volume(0.5, 0.0, 1.0, 0.1)
        self.sfx_volume = volume(0.7, 0.0, 1.0, 0.1)

    def run(self):
        Option_run = True
        while Option_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Option_run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # get mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    if self.volume_button.is_clicked(mouse_pos):
                        print("Music volume:", self.music_volume.get_volume())
                        print("SFX volume:", self.sfx_volume.get_volume())
                        volume.run()  # assuming there's a run_volume function in volume
                    elif self.display_button.is_clicked(mouse_pos):
                        display.run()  # assuming there's a run_display function in display
                    elif self.back_button.is_clicked(mouse_pos):
                        Option_run = False

            self.screen.fill(BLACK)
            # Draw the button
            self.volume_button.draw(self.screen)
            self.display_button.draw(self.screen)
            self.back_button.draw(self.screen)

            # Update every second
            pygame.display.flip()
            # Update the display
            pygame.display.update()

            # Tick the clock to control the frame rate
            self.clock.tick(120)

        # Quit Pygame
        pygame.quit()
    
option = Option
option.run()

