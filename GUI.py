import pygame
from setting import *
from button import Button
import option
import main 
import help

class GUI:
    def __init__(self):
        pygame.init()

        # Set the dimensions of the screen
        self.screen = pygame.display.set_mode((screenwidth, screenheight))

        self.clock = pygame.time.Clock()

        #define the button    
        self.start_button = Button(320,"Start",WHITE)
        self.option_button = Button(420,"Option",WHITE)
        self.help_button = Button(520,"Help",WHITE)
        self.quit_button = Button(620,"Quit",WHITE)

    def run(self):
        game_running = True
        while game_running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # get mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button.is_clicked(mouse_pos):
                        main.run()
                    elif self.option_button.is_clicked(mouse_pos):
                        option.run() 
                    elif self.help_button.is_clicked(mouse_pos):
                        help.run()
                    elif self.quit_button.is_clicked(mouse_pos):
                        game_running = False

            self.screen.fill(BLACK)
            # Draw the button
            self.start_button.draw(self.screen)
            self.option_button.draw(self.screen)
            self.help_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            
            # Update every second
            pygame.display.flip()
            # Update the display
            pygame.display.update()

            # Tick the clock to control the frame rate
            self.clock.tick(120)

        # Quit Pygame
        if pygame.display.get_surface() is not None:
            pygame.display.quit()
        pygame.quit()

if __name__ == '__main__':
     game = GUI()
     game.run()
