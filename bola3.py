import random
import math
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class MainBall(pygame.sprite.Sprite):
    def __init__(self, color, x, y, radius, speed):
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
        elif self.rect.right > SCREEN_WIDTH:
            self.direction = 180 - self.direction
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.direction = 360 - self.direction
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.direction = 360 - self.direction
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlackBall(MainBall):
    def __init__(self, x, y):
        super().__init__((0, 0, 0), x, y, 10, 5)
        self.start_direction = self.direction

        # Define the track of the black ball
        self.track_points = [(50, 300), (400, 300), (400, 150), (750, 150), (750, 50)]
        self.track_idx = 0
        self.track_dir = 1
        self.track_rect = pygame.Rect(*self.track_points[0], 10, 10) 

    def update(self, all_balls):
        super().update(other_balls = all_balls)

        # Check if the black ball is at the end of the track
        if self.track_idx == len(self.track_points) - 2:
            self.track_dir = -1
        elif self.track_idx == 0 and self.track_dir == -1:
            self.track_dir = 1

        # Move the black ball along the track
        self.track_rect.move_ip(self.track_dir * self.speed, 0)

        if self.track_dir == 1:
            if self.track_rect.right > self.track_points[self.track_idx+1][0]:
                self.track_idx += 1
        else:
            print([self.track_idx+1])
            if self.track_rect.left < self.track_points[self.track_idx+1][0]:
                self.track_idx += 1

        # Update the position of the black ball
        if self.track_idx == len(self.track_points) - 1:
            self.rect.left = -self.radius
        elif self.track_idx == 0:
            self.rect.top = self.track_rect.top
            self.rect.left = self.track_rect.left
        else:
            self.rect.centerx = self.track_rect.centerx
            self.rect.centery = self.track_rect.centery

        # Update the direction of the black ball
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction = 180 - self.start_direction
        if self.rect.top < 0:
            self.direction = 360 - self.start_direction
        if self.rect.bottom > SCREEN_HEIGHT:
            self.direction = 180 - self.start_direction


class WhiteBall(MainBall):
    def __init__(self, x, y):
        super().__init__((0, 0, 255), x, y, 10, 5)

    def update(self, other_balls):
        super().update(other_balls)

        # Bounce off walls
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 180 - self.direction
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = 180 - self.direction
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction = 360 - self.direction
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.direction = 360 - self.direction

        # Bounce off black ball
        # for ball in other_balls:
        #     if isinstance(ball, BlackBall) and pygame.sprite.collide_circle(self, ball):
        #         self.direction = random.randint(0, 360)

        # Bounce off white balls
        for ball in other_balls:
            if isinstance(ball, WhiteBall) and ball != self and pygame.sprite.collide_circle(self, ball):
                self.direction = random.randint(0, 360)

    # def update(self, other_balls):
    #     super().update(other_balls)

    #     # Bounce off walls
    #     if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
    #         self.direction = 180 - self.direction
    #     if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
    #         self.direction = 360 - self.direction

    #     # Bounce off black ball
    #     for ball in other_balls:
    #         if isinstance(ball, BlackBall) and pygame.sprite.collide_circle(self, ball):
    #             self.direction = random.randint(0, 360)


# Below is backup code 

# class BlackBall(MainBall):
#     def __init__(self, x, y):
#         super().__init__((0, 0, 0), x, y, 10, 5)
#         self.start_direction = self.direction

#     def update(self, other_balls):
#         super().update(other_balls)

#         # Reverse direction if black ball reaches end of path
#         if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
#             self.direction = 180 - self.start_direction
#         if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
#             self.direction = 360 - self.start_direction

# class WhiteBall(MainBall):
#     def __init__(self, x, y):
#         super().__init__((0, 0, 255), x, y, 10, 5)

#     def update(self, other_balls):
#         super().update(other_balls)

#         # Bounce off walls
#         if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
#             self.direction = 180 - self.direction
#         if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
#             self.direction = 360 - self.direction

#         # Bounce off black ball
#         for ball in other_balls:
#             if isinstance(ball, BlackBall) and pygame.sprite.collide_circle(self, ball):
#                 self.direction = random.randint(0, 360)

# Dibawah ini backup method update lama dari MainBall
    # def update(self, other_balls):
    #     # Move the ball in its direction
    #     dx = self.speed * round(math.cos(math.radians(self.direction)), 2)
    #     dy = self.speed * round(math.sin(math.radians(self.direction)), 2)
    #     self.rect.move_ip(dx, dy)

    #     # Check if the ball hit the wall
    #     if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
    #         self.direction = 180 - self.direction
    #     if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
    #         self.direction = 360 - self.direction

    #     # Check if the ball hit another ball
    #     for ball in other_balls:
    #         if self != ball and pygame.sprite.collide_circle(self, ball):
    #             self.direction = random.randint(0, 360)