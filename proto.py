import pygame
import random
from setting import *

class MainBall(pygame.sprite.Sprite):
    def __init__(self, color, x, y, radius, speed):
        # x and y is the position of the ball
        super().__init__()

        # Set the ball's properties
        self.color = color
        self.radius = radius
        self.speed = speed

        # Create the ball's surface and rect
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))

        # Set the ball's direction randomly
        self.direction = random.randint(0, 360)

    def update(self, other_balls, track_rect=None):
        if track_rect and not self.rect.colliderect(track_rect):
            return

        # Move the ball in the current direction
        dx = self.speed * math.cos(math.radians(self.direction))
        dy = self.speed * math.sin(math.radians(self.direction))
        self.rect.move_ip(dx, dy)

        # Check if the ball collides with other balls
        for ball in other_balls:
            if self == ball:
                continue
            if self.rect.colliderect(ball.rect):
                angle = math.atan2(self.rect.centery - ball.rect.centery,
                                   self.rect.centerx - ball.rect.centerx)
                angle = math.degrees(angle)
                self.direction = 2 * angle - self.direction
                ball.direction = 2 * angle - ball.direction

        # Check if the ball collides with the edges of the screen
        if self.rect.left < 0:
            self.direction = 180 - self.direction
            self.rect.left = 0
        elif self.rect.right > screenwidth:
            self.direction = 180 - self.direction
            self.rect.right = screenwidth
        if self.rect.top < 0:
            self.direction = 360 - self.direction
            self.rect.top = 0
        elif self.rect.bottom > screenheight:
            self.direction = 360 - self.direction
            self.rect.bottom = screenheight

    def draw(self, surface):
        surface.blit(self.image, self.rect)
class WhiteBall(MainBall):
    def __init__(self, x, y):
        super().__init__((0, 0, 255), x, y, 25, 5)

    def update(self, other_balls):
        super().update(other_balls)
        # Bounce off walls
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 180 - self.direction
        elif self.rect.right > screenwidth:
            self.rect.right = screenwidth
            self.direction = 180 - self.direction
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction = 360 - self.direction
        elif self.rect.bottom > screenheight:
            self.rect.bottom = screenheight
            self.direction = 360 - self.direction
        # Bounce of white balls
        for ball in other_balls:
            if isinstance(ball, WhiteBall) and ball != self and pygame.sprite.collide_circle(self, ball):
                self.direction = random.randint(0, 360)

        # # Slow down over time
        # if self.speed > 0:
        #     self.speed -= 0.005
        #     # print("Current speed:", self.speed)
        # # Stop the ball completely
        # elif self.speed <=0:
        #     self.speed = 0

class CollidingRect(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, ballarrayinput, num_rows, num_columns):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.set_alpha(128)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        # Center the rectangle at the given position
        self.rect.center = (x, y)

        self.ballarray_colliding = []

        # Create 2D array of white balls
        self.ballarray = []
        for row in range(num_rows):
            row_balls = []
            for col in range(num_columns):
                ball = None
                for sprite in ballarrayinput.sprites():
                    if isinstance(sprite, WhiteBall) and pygame.sprite.collide_rect(sprite, self):
                        ball = sprite
                        break
                if ball:
                    ball_x = x - width//2 + (col + 0.5) * (width // num_columns)
                    ball_y = y - height//2 + (row + 0.5) * (height // num_rows)
                    ball.rect.center = (ball_x, ball_y)
                    row_balls.append(ball)
            self.ballarray.append(row_balls)

    def update(self, ballarray):
        self.ballarray_colliding = []
        for ball in ballarray.sprites():
            if isinstance(ball, WhiteBall) and pygame.sprite.collide_rect(self, ball):
                self.ballarray_colliding.append(ball)
                if ball not in self.ballarray:
                    self.ballarray.append(ball)
                    print(ballarray)
                # if len(self.ballarray_colliding) == 3:
                #     self.ballarray= []
                else:
                    if ball.rect.left < self.rect.left:
                        ball.rect.left = self.rect.left
                    elif ball.rect.right > self.rect.right:
                        ball.rect.right = self.rect.right
                    if ball.rect.top < self.rect.top:
                        ball.rect.top = self.rect.top
                    elif ball.rect.bottom > self.rect.bottom:
                        ball.rect.bottom = self.rect.bottom
                     # Remove and kill the ball if it collides with the rectangle
                    if pygame.sprite.collide_rect(self, ball):
                        self.ballarray.remove(ball)
                    ball.kill()

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode([screenwidth, screenheight])
pygame.display.set_caption("Colliding Rect and White Balls")

# Set up the clock
clock = pygame.time.Clock()

# Create some balls
white_ball1 = WhiteBall(screenwidth * 0.75, screenheight * 0.75)
white_ball2 = WhiteBall(screenwidth * 0.25, screenheight * 0.25)
white_ball3 = WhiteBall(screenwidth * 0.5, screenheight * 0.5)
white_ball4 = WhiteBall(screenwidth , screenheight)
white_balls = pygame.sprite.Group()
white_balls.add(white_ball1)
white_balls.add(white_ball2)
white_balls.add(white_ball3)
white_balls.add(white_ball4)

# Create a colliding rectangle
colliding_rect =  CollidingRect(screenwidth*0.5, screenheight*0.5, 200, 200,white_balls, 2, 2)
colliding_rect_group = pygame.sprite.Group()
colliding_rect_group.add(colliding_rect)

done = False
while not done:
# Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Update the game state
    white_balls.update(white_balls)
    colliding_rect.update(white_balls)

    # Draw everything
    screen.fill(BLACK)
    for ball in white_balls:
        pygame.draw.circle(screen, ball.color, ball.rect.center, ball.radius)
    pygame.draw.rect(screen, BLUE, colliding_rect.rect, 2)
    for ball in colliding_rect.ballarray_colliding:
        pygame.draw.circle(screen, BLUE, ball.rect.center, ball.radius, 2)

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(60)

pygame.quit()

