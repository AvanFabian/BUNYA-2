import pygame
from bola3 import BlackBall, C, O, H
from setting import *

class Elemenyer(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, ballarrayinput, num_rows, num_columns):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.set_alpha(128)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.black_ball_counter = 0  # counter for number of black balls collided with rectangle
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
                    if (isinstance(sprite, BlackBall) or isinstance(sprite, C) or
                        isinstance(sprite, O) or isinstance(sprite, H)) and pygame.sprite.collide_rect(sprite, self):
                        ball = sprite
                        break
                if ball:
                    ball_x = x - width//2 + (col + 0.5) * (width // num_columns)
                    ball_y = y - height//2 + (row + 0.5) * (height // num_rows)
                    ball.rect.center = (ball_x, ball_y)
                    row_balls.append(ball)
            self.ballarray.append(row_balls)

    def update(self, ballarray, score):
        self.ballarray_colliding = []
        for ball in ballarray.sprites():
            if isinstance(ball, BlackBall) and pygame.sprite.collide_rect(self, ball):
                self.ballarray_colliding.append("BlackBall")
            elif isinstance(ball, O) and pygame.sprite.collide_rect(self, ball):
                self.ballarray_colliding.append("O")
            elif isinstance(ball, H) and pygame.sprite.collide_rect(self, ball):
                self.ballarray_colliding.append("H")
            elif isinstance(ball, C) and pygame.sprite.collide_rect(self, ball):
                self.ballarray_colliding.append("C")
                if ball not in self.ballarray:
                    self.ballarray.append(ball)
                    self.black_ball_counter += 1
                    if len(self.ballarray_colliding) >= 3:
                        if self.ballarray_colliding.count("O") == 2 and self.ballarray_colliding.count("H") == 1:
                            score.add_score(5)
                        elif self.ballarray_colliding.count("C") == 2 and self.ballarray_colliding.count("O") == 1:
                            score.add_score(5)
                        else:
                            score.add_score(3)
                        for ball_inside in self.ballarray:
                            if (isinstance(ball_inside, BlackBall) or isinstance(ball_inside, O) 
                                or isinstance(ball_inside, C) or isinstance(ball_inside, H)):
                                ballarray.remove(ball_inside)
                                ball_inside.kill()
                        self.ballarray = []
                        self.black_ball_counter = 0
                        score.add_score(3)  # Increase the score by 3
                else:
                    if ball.rect.left < self.rect.left:
                        ball.rect.left = self.rect.left
                    elif ball.rect.right > self.rect.right:
                        ball.rect.right = self.rect.right
                    if ball.rect.top < self.rect.top:
                        ball.rect.top = self.rect.top
                    elif ball.rect.bottom > self.rect.bottom:
                        ball.rect.bottom = self.rect.bottom

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect, 2)

class Score(pygame.sprite.Sprite):
    def __init__(self, initial_score=0):
        super().__init__()
        self.score = initial_score
        self.font = pygame.font.Font(None, 36)
        self.color = WHITE
        self.update()

    def update(self):
        self.image = self.font.render(f"Score: {self.score}", True, self.color)
        self.rect = self.image.get_rect()

    def add_score(self, points):
        self.score += points
        self.update()

    def reset_score(self):
        self.score = 0
        self.update()

    def draw(self, surface):
        surface.blit(self.image, (1080, 10))  # blit the score image onto the specified surface