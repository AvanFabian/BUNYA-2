import pygame

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
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.collision_box = self.image.get_rect()  # Use the sprite image's rect as the collision box
        self.collision_box.center = self.rect.center  # Position the collision box at the center of the sprite
        self.velocity = [0, 0]
        self.gravity = 0.5
        self.max_jump_height = 100
        self.jump_speed = -10
        self.is_jumping = False
        self.jump_start_pos = None

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.collision_box.center = self.rect.center  # Update the position of the collision box to match the sprite

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.collision_box, 2)

    def update_image(self, image_path):
        self.image = pygame.image.load("HIDROGEN.png").convert_alpha()


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

# Set up the game loop
game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character.update_image(character_images["up"])
                character.move(0, -1)
            elif event.key == pygame.K_DOWN:
                character.update_image(character_images["down"])
                character.move(0, 1)
            elif event.key == pygame.K_LEFT:
                character.update_image(character_images["left"])
                character.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                character.update_image(character_images["right"])
                character.move(1, 0)
            elif event.key == pygame.K_UP and event.key == pygame.K_LEFT:
                character.update_image(character_images["up_left"])
                character.move(-1, -1)
            elif event.key == pygame.K_UP and event.key == pygame.K_RIGHT:
                character.update_image(character_images["up_right"])
                character.move(1, -1)
            elif event.key == pygame.K_DOWN and event.key == pygame.K_LEFT:
                character.update_image(character_images["down_left"])
                character.move(-1, 1)
            elif event.key == pygame.K_DOWN and event.key == pygame.K_RIGHT:
                character.update_image(character_images["down_right"])
                character.move(1, 1)
            elif event.key == pygame.K_SPACE and not character.is_jumping:
                character.is_jumping = True
                character.velocity[1] = character.jump_speed
        # Apply gravity to the player
        character.velocity[1] += character.gravity

        # Move the player
        character.rect.move_ip(character.velocity)

        # Check if the player hits the bottom of the screen
        if player_rect.bottom >= window_size[1]:
            player_rect.bottom = window_size[1]
            player_velocity[1] = 0
            player_is_jumping = False

        # Limit the player's jump based on the maximum jump height
        if player_is_jumping and player_rect.bottom <= player_jump_start_pos - player_max_jump_height:
            player_is_jumping = False

        # Handle keyboard input for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_velocity[0] = -5
        elif keys[pygame.K_RIGHT]:
            player_velocity[0] = 5
        else:
            player_velocity[0] = 0

    # Update the game state

    # Draw the game world
    game_display.fill((255, 255, 255))  # Fill the display with white
    all_sprites.draw(game_display)  # Draw all sprites
    # Update the display
    pygame.display.update()

    # Tick the clock to control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
