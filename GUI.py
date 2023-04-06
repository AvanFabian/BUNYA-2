import pygame
from setting import * 
import sys

pygame.init()

# Set the dimensions of the screen
screen = pygame.display.set_mode((screenwidth, screenheight))

# Set the font for the buttons
font = pygame.font.SysFont("Arial", 40)

# Set up the game clock
clock = pygame.time.Clock()

class Button:
    def __init__(self, y, text, bg_color, initial_volume=0.5, min_volume=0.0, max_volume=1.0, step=0.1):
        # self.image = pygame.image.load(image_path)
        # self.rect = self.image.get_rect()
        # self.rect.topleft = (screenwidth/2 - self.width/2, y - self.height/2)
        self.width = 200
        self.height = 50
        self.rect = pygame.Rect(screenwidth/2 - self.width/2, y - self.height/2, self.width, self.height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', 32)
        self.font_color = BLACK
        self.bg_color = bg_color


    def draw(self, surface):
        # surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    

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
                from option import  *
            elif help_button.is_clicked(mouse_pos):
                from help import *
            elif quit_button.is_clicked(mouse_pos):
                pygame.quit()
       
    
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
pygame.quit()
