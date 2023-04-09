import pygame
from setting import *
from button import Button

class GUI:
    def __init__(self):
        pygame.init()

        # Set the dimensions of the screen
        self.screen = pygame.display.set_mode((screenwidth, screenheight))

        self.clock = pygame.time.Clock()
        # Set the window title
        pygame.display.set_caption("Bunya: Mari buat senyawa")

        # Stage background
        self.background = pygame.image.load("assets/bg_stage.png").convert()


        #define the button    
        self.start_button = Button(320,"Start",WHITE)
        self.option_button = Button(420,"Option",WHITE)
        self.help_button = Button(520,"Help",WHITE)
        self.quit_button = Button(620,"Quit",WHITE)
        
        #define class
        self.option = Option()
        self.help = Help()

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
                        import main
                        main.run()
                    elif self.option_button.is_clicked(mouse_pos):
                        self.option.run() 
                    elif self.help_button.is_clicked(mouse_pos):
                        self.help.run()
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
            self.clock.tick(60)

        # Quit Pygame
        if pygame.display.get_surface() is not None:
            pygame.display.quit()
        pygame.quit()

class Option:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((screenwidth, screenheight))
        self.clock = pygame.time.Clock()
        # Set the window title
        pygame.display.set_caption("Bunya: Mari buat senyawa")

        self.back_button = Button(520, "Back", WHITE)
        self.display_button = Button(420, "Display", WHITE)
        
        self.display = Display()

    def run(self):
        Option_run = True
        while Option_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Option_run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # get mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    if self.display_button.is_clicked(mouse_pos):
                       self.display.run()
                    elif self.back_button.is_clicked(mouse_pos):
                        Option_run = False
                        

            self.screen.fill(BLACK)
            # Draw the button
            self.display_button.draw(self.screen)
            self.back_button.draw(self.screen)

            # Update every second
            pygame.display.flip()
            # Update the display
            pygame.display.update()

            # Tick the clock to control the frame rate
            self.clock.tick(60)


class Display:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((screenwidth, screenheight))

        # Set up the game clock
        self.clock = pygame.time.Clock()

        # Set the window title
        pygame.display.set_caption("Bunya: Mari buat senyawa")


        # Create checkbox rect and font
        self.checkbox_rect = pygame.Rect(50, 50, 20, 20)
        self.checkbox_font = pygame.font.SysFont(None, 24)
        self.back_button = Button(520,"Back",WHITE)
    
    def run(self):
        # Run the game loop
        display_run=True
        while display_run:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display_run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        if self.checkbox_rect.collidepoint(event.pos):
                            # Toggle full screen
                            if self.screen.get_flags() & pygame.FULLSCREEN:
                                pygame.display.set_mode((screenwidth, screenheight))
                            else:
                                pygame.display.set_mode((screenwidth, screenheight), pygame.FULLSCREEN)
                        elif self.back_button.is_clicked(mouse_pos):
                            display_run = False
                        

            # Clear the screen
            self.screen.fill(WHITE)

            # Draw the checkbox
            pygame.draw.rect(self.screen, BLACK, self.checkbox_rect, 2)
            if self.screen.get_flags() & pygame.FULLSCREEN:
                pygame.draw.line(self.screen, BLACK, (self.checkbox_rect.left + 3, self.checkbox_rect.centery), (self.checkbox_rect.right - 3, self.checkbox_rect.centery), 3)
            self.back_button.draw(self.screen)
            # Draw the label
            label_text = "Full Screen"
            if self.screen.get_flags() & pygame.FULLSCREEN:
                label_text += " (ON)"
            else:
                label_text += " (OFF)"
            label_surface = self.checkbox_font.render(label_text, True, BLACK)
            label_rect = label_surface.get_rect(midleft=(self.checkbox_rect.right + 10, self.checkbox_rect.centery))
            self.screen.blit(label_surface, label_rect)

            # Update the display
            pygame.display.update()

            # Tick the clock to control the frame rate
            self.clock.tick(120)
class Help:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screenwidth, screenheight))
        self.clock = pygame.time.Clock()
        self.slideshow_images = []
        self.current_image_index = 0
        self.back_button = Button(520,"Back",WHITE)
        # Set the window title
        pygame.display.set_caption("Bunya: Mari buat senyawa")


    def load_images(self):
        with open('help.txt', 'r') as f:
            for line in f:
                line = line.strip()
                try:
                    image = pygame.image.load(line)
                    self.slideshow_images.append(image)
                except Exception as e:
                    print(f"Error loading image '{line}': {e}")

    def run(self):
        self.load_images()
        help_running = True
        while help_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    help_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.current_image_index += 1
                    mouse_pos = pygame.mouse.get_pos()
                    if self.current_image_index >= len(self.slideshow_images):
                        self.current_image_index = 0
                    elif self.back_button.is_clicked(mouse_pos):
                        help_running = False

            self.screen.fill(BLACK)
            screen_center = (screenwidth // 2, screenheight // 2)
            image_center = self.slideshow_images[self.current_image_index].get_rect().center
            offset = (screen_center[0] - image_center[0], screen_center[1] - image_center[1])
            self.screen.blit(self.slideshow_images[self.current_image_index], offset)
            self.back_button.draw(self.screen)
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
     game = GUI()
     game.run()


