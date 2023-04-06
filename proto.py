import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Define the size of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the size and position of the rectangle
RECTANGLE_WIDTH = 200
RECTANGLE_HEIGHT = 300
RECTANGLE_X = 100
RECTANGLE_Y = 50

# Create a surface to draw the rectangle on
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define a Sprite class
class MySprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.0001

    def update(self, target_rect):
        print(f"Sprite at ({self.rect.x}, {self.rect.y}) targeting rectangle at ({target_rect.x}, {target_rect.y})")
        dx = target_rect.x - self.rect.x
        dy = target_rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist > self.speed:
            self.rect.x += dx / dist * self.speed
            self.rect.y += dy / dist * self.speed
        else:
            self.rect.x = target_rect.x
            self.rect.y = target_rect.y
        print(f"New position: ({self.rect.x}, {self.rect.y})")

# Create a Group container
sprite_group = pygame.sprite.Group()

# Spawn some sprites randomly in one of the four corners of the screen
for i in range(10):
    x = random.choice([0, SCREEN_WIDTH])
    y = random.choice([0, SCREEN_HEIGHT])
    if x == 0 and y == 0:
        x += 50
        y += 50
    elif x == SCREEN_WIDTH and y == 0:
        x -= 50
        y += 50
    elif x == 0 and y == SCREEN_HEIGHT:
        x += 50
        y -= 50
    else:
        x -= 50
        y -= 50
    sprite = MySprite(x, y)
    sprite_group.add(sprite)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the sprites
    for sprite in sprite_group:
        sprite.update(pygame.Rect(RECTANGLE_X, RECTANGLE_Y, RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
        print(f"---")

    # Draw the rectangle and the sprites on the screen
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 255, 0), (RECTANGLE_X, RECTANGLE_Y, RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
    sprite_group.draw(screen)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
