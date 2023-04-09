import pygame
from setting import *
from button import Button, Volume

class BrightnessControl:
    def __init__(self):
        self.brightness = 255

class Display:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((screenwidth, screenheight))

        # Set up the game clock
        self.clock = pygame.time.Clock()

        # Create checkbox rect and font
        self.checkbox_rect = pygame.Rect(50, 50, 20, 20)
        self.checkbox_font = pygame.font.SysFont(None, 24)
        self.back_button = Button(520,"Back",WHITE)
    
    def run(self):
        # Run the game loop
        display_run = True
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
            self.clock.tick(60)

        # Quit Pygame
        pygame.quit()
display = Display
display.run()