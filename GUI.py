import pygame
from setting import width as screen_width, height as screen_height
pygame.init()

# Set the dimensions of the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the font for the buttons
font = pygame.font.SysFont("Arial", 40)

# Define the colors to be used
white = (255, 255, 255)
black = (0, 0, 0)

# Create the buttons
start_button = font.render("Start", True, black, white)
help_button = font.render("Help", True, black, white)
options_button = font.render("Options", True, black, white)
quit_button = font.render("Quit", True, black, white)

# Set the coordinates for the buttons
start_button_rect = start_button.get_rect(center=(screen_width/2, screen_height/4))
help_button_rect = help_button.get_rect(center=(screen_width/2, screen_height/2))
options_button_rect = options_button.get_rect(center=(screen_width/2, 3*screen_height/4))
quit_button_rect = quit_button.get_rect(center=(screen_width/2, 7*screen_height/8))

# Define the function for the help screen
def help_screen():
    # Create a list of images to be displayed in the slideshow
    images = ["instruction1.png", "instruction2.png", "instruction3.png"]
    index = 0

    # Loop through the list of images and display them on the screen
    while True:
        # Load the current image and scale it to fit the screen
        image = pygame.image.load(images[index]).convert()
        image = pygame.transform.scale(image, (screen_width, screen_height))

        # Display the image on the screen
        screen.blit(image, (0, 0))
        pygame.display.flip()

        # Wait for a key press or the quit event
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                return

        # Increment the index to display the next image
        index = (index + 1) % len(images)

# Define the function for the GUI
def main_menu():
    while True:
        # Display the buttons on the screen
        screen.fill(white)
        screen.blit(start_button, start_button_rect)
        screen.blit(help_button, help_button_rect)
        screen.blit(options_button, options_button_rect)
        screen.blit(quit_button, quit_button_rect)
        pygame.display.flip()

        # Check for button clicks or the quit event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    print("Start button clicked")
                elif help_button_rect.collidepoint(event.pos):
                    print("Help button clicked")
                elif options_button_rect.collidepoint(event.pos):
                    print("option button clicked")
                elif quit_button_rect.collidepoint(event.pos):
                    print("Quit button clicked")
            elif event.type == pygame.QUIT:
                pygame.quit()
                return

# Run the GUI
main_menu()
