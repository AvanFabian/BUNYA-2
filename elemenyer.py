import pygame
from bola3 import BlackBall
from setting import *

class Elemenyer(pygame.sprite.Sprite):
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
                    if isinstance(sprite, BlackBall) and pygame.sprite.collide_rect(sprite, self):
                        ball = sprite
                        break
                if ball:
                    ball_x = x - width//2 + (col + 0.5) * (width // num_columns)
                    ball_y = y - height//2 + (row + 0.5) * (height // num_rows)
                    ball.rect.center = (ball_x, ball_y)
                    row_balls.append(ball)
            self.ballarray.append(row_balls)

        # Debug output
        # print(f"Created Elemenyer at ({x}, {y}) with {len(self.ballarray)} rows and {len(self.ballarray[0])} columns")
        # print(f"Initial ballarray: {ballarrayinput}")
        # print(f"Initial ballarray colliding with Elemenyer: {self.ballarray_colliding}")
        # print(f"Initial ballarray inside Elemenyer: {self.ballarray}")

    def update(self, ballarray):
        self.ballarray_colliding = []
        for ball in ballarray.sprites():
            if isinstance(ball, BlackBall) and pygame.sprite.collide_rect(self, ball):
                self.ballarray_colliding.append(ball)
                if ball not in self.ballarray:
                    self.ballarray.append(ball)
                    # Debug output
                    print(f"Added ball {ball} to Elemenyer at ({self.rect.centerx}, {self.rect.centery})")
                    print(f"Updated ballarray inside Elemenyer: {self.ballarray}")
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
                    # if pygame.sprite.collide_rect(self, ball):
                    #     self.ballarray.remove(ball)
                    #     # Debug output
                    #     print(f"Removed ball {ball} from Elemenyer at ({self.rect.centerx}, {self.rect.centery})")
                    # ball.kill()

        # Debug output
        # print(f"Updated ballarray colliding with Elemenyer: {self.ballarray_colliding}")
        # print(f"Final ballarray inside Elemenyer: {self.ballarray}")
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect, 2)
