import pygame
from bola3 import MainBall, BlackBall, WhiteBall

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))

# Set the window title
pygame.display.set_caption("My Game")


# Define the character sprite class
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("HIDROGEN.png").convert_alpha()  # Load the sprite image
        self.rect = self.image.get_rect() # Use the image's rect as the sprite's rect
        self.rect.center = (x, y)
        self.speed = 5
        self.collision_box = self.image.get_rect()  # Use the sprite image's rect as the collision box
        self.collision_box.center = self.rect.center  # Position the collision box at the center of the sprite

         # Set initial values for movement flags
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        #initial jump method
        self.jump_size = 50  # Increase in height when jumping
        self.jump_duration = 30  # Duration of jump in frames
        self.jump_timer = 0  # Timer for tracking jump duration
        self.jump_flag = False  # Flag to indicate whether the character is jumping

    #moving of the character
    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.collision_box.center = self.rect.center  # Update the position of the collision box to match the sprite

    #display the character drawing
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.collision_box, 2) 

    #Updating image of character
    def update_image(self, image_path):
        self.image = pygame.image.load("HIDROGEN.png").convert_alpha()

    #Movement of character
    def movement(self):
        if  self.move_up:
            print("ke atas")
            self.update_image(character_images["up"])
            self.move(0, -1)
        elif self.move_down:
            print("ke bawah")
            self.update_image(character_images["down"])
            self.move(0, 1)
        elif self.move_right:
            print("ke kanan")
            self.update_image(character_images["right"])
            self.move(1, 0)
        elif self.move_left:
            print("ke kiri")
            self.update_image(character_images["left"])
            self.move(-1, 0)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move_up = True
            elif event.key == pygame.K_DOWN:
                self.move_down = True
            elif event.key == pygame.K_LEFT:
                self.move_left = True
            elif event.key == pygame.K_RIGHT:
                self.move_right = True
            elif event.key == pygame.K_SPACE:
                self.character.jump()  # Call the jump method when the up arrow is pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.move_up = False
            elif event.key == pygame.K_DOWN:
                self.move_down = False
            elif event.key == pygame.K_LEFT:
                self.move_left = False
            elif event.key == pygame.K_RIGHT:
                self.move_right = False  

    #Make character jump              
    def jump(self):
        if not self.jump_flag:
            self.jump_flag = True
            self.rect.height += self.jump_size  # Increase the height of the character
            self.collision_box.height = self.rect.height  # Adjust the collision box
            self.jump_timer = 0
    
    def update(self):
        # ...
        if self.jump_flag:
            # Increase the jump timer
            self.jump_timer += 1

            # If the jump duration is over, disable the jump flag and reset the size of the character
            if self.jump_timer >= self.jump_duration:
                self.jump_flag = False
                self.rect.height -= self.jump_size
                self.collision_box.height = self.rect.height 

    def detect_collisions(self):
        if not self.character.jump_flag:  # Skip collision detection if the character is jumping
            return 0
    
         
      
# Set up the game clock
clock = pygame.time.Clock()

# Load the character sprites for each direction
character_images = dict(up="HIDROGEN.png", down="HIDROGEN.png", left="HIDROGEN.png", right="HIDROGEN.png",
                        up_left="HIDROGEN.png", up_right="HIDROGEN.png", down_left="HIDROGEN.png",
                        down_right="HIDROGEN.png")

# Create the character sprite and add it to a sprite group
character = Character(display_width / 2, display_height / 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(character) 

# Create the balls
black_balls = [BlackBall(50, 50), BlackBall(display_width - 50, 50), BlackBall(50, display_height - 50), BlackBall(display_width - 50, display_height - 50)]
white_balls = [WhiteBall(100, 100), WhiteBall(display_width - 100, 100), WhiteBall(100, display_height - 100), WhiteBall(display_width - 100, display_height - 100)]

# Add the balls to sprite groups
all_balls = pygame.sprite.Group()
# all_balls.add(main_ball)
all_balls.add(black_balls)
all_balls.add(white_balls)


# Set up the game loop
game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        #event when quit pressed
        if event.type == pygame.QUIT:
            game_running = False
        #event when button pressed 
        elif event:
            character.handle_event(event) 
        

    character.movement()  # Call the movement method of the character

    # Update the balls
    all_balls.update(all_balls)

    # Draw the game world
    game_display.fill((255, 255, 255))  # Fill the display with white
    all_sprites.draw(game_display)  # Draw all sprites
    character.draw(game_display)
    # Draw the balls
    all_balls.draw(game_display)
    
    # Update the display
    pygame.display.update()

    # Tick the clock to control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
