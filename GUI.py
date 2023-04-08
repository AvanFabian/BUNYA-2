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

#---------------------------------------------------------------------------------------------------------------------

#class Game:
#     def __init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((screenwidth, screenheight))
#         self.clock = pygame.time.Clock()
#         self.ball_container = BallContainer()
    
#     def run(self):
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
            
#             self.screen.fill(BLACK)
#             # Update and draw the ball container
#             self.ball_container.update()
#             self.ball_container.draw(self.screen)
            
#             pygame.display.flip()
#             pygame.display.update()
#             self.clock.tick(60)
        
#         pygame.quit()

# if __name__ == '__main__':
#     game = Game()
#     game.run()

#--------------------------------------------------------------------------------------------------------

# class PygameWindow:
#     def __init__(self, width=640, height=480, title="Pygame Window"):
#         # Initialize Pygame
#         pygame.init()

#         # Set the dimensions of the window
#         self.width = width
#         self.height = height

#         # Create the window
#         self.win = pygame.display.set_mode((self.width, self.height))

#         # Set the title of the window
#         pygame.display.set_caption(title)

#     def run(self):
#         # Run the game loop
#         while True:

#             # Handle events
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     quit()

#             # Fill the window with black
#             self.win.fill((0, 0, 0))

#             # Update the window
#             pygame.display.update()

# window = PygameWindow(width=800, height=600, title="My Custom Pygame Window")
# window.run()
