import random
import math
import time
import pygame
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
        print(f"MainBall rect: {self.rect}")


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

    def bounce_walls(self):
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


    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlackBall(MainBall):

    def __init__(self, x, y):
        super().__init__((0, 0, 0), x, y, 25, 5)
        self.start_direction = self.direction

        # Define the track of the black ball
        # self.track_points = [(screenwidth / 3.0, screenheight), (screenwidth / 3.0, 0)]
        self.track_points = [
                        (screenwidth / 2.3, screenheight),
                        (screenwidth / 2.3, screenheight/1.2),
                        (screenwidth / 2.3, screenheight/1.35),
                        (screenwidth / 2.0, screenheight/1.7),
                        (screenwidth * 1.6 / 3.0, screenheight / 2.0),
                        (screenwidth * 1.7 / 3.0, screenheight / 2.0),
                        (screenwidth * 1.8 / 3.0, screenheight / 2.0),
                        (screenwidth * 1.9 / 3.0, screenheight / 2.0),
                        (screenwidth * 2.0 / 3.0, screenheight / 2.0),
                        (screenwidth * 2.1 / 3.0, screenheight / 2.0),
                        (screenwidth * 2.3 / 3.0, screenheight / 2.0),
                        (screenwidth, screenheight / 2.1)]

        self.track_idx = 0
        self.track_dir = 1

        # Create a rect to represent the black ball's position on the track
        # '*' is for unpacking the tuple
        self.track_rect = pygame.Rect(*self.track_points[0], 20, 20)
        self.track_rect = pygame.Rect(*self.track_points[self.track_idx], 1, 1)
        self.start_direction = self.start_direction
        self.direction = self.start_direction
        self.speed = 4 # speed of the black ball
        self.on_track = True # is the black ball on the track?

    def update(self, other_balls):
        if self.on_track:
            # Move the black ball along the track
            if self.track_idx == 0:
                self.track_dir = 1
            elif self.track_idx == len(self.track_points) - 1:
                self.track_dir = -1

            # Calculate the distance and angle to the next track point
            next_point = self.track_points[self.track_idx + self.track_dir]
            dx = next_point[0] - self.track_rect.centerx
            dy = next_point[1] - self.track_rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            angle = math.degrees(math.atan2(dy, dx))

            # Gradually move the ball towards the next track point
            if distance < self.speed:
                self.track_idx += self.track_dir
                self.track_rect.center = self.track_points[self.track_idx]
            else:
                self.track_rect.centerx += self.speed * math.cos(math.radians(angle))
                self.track_rect.centery += self.speed * math.sin(math.radians(angle))

            # Update the black ball's direction when it reaches a track point
            if self.track_idx == 0:
                self.direction = 180 - self.start_direction
            elif self.track_idx == len(self.track_points) - 1:
                self.direction = 360 - self.start_direction

            # Update the black ball's position
            self.rect.center = self.track_rect.center

            # Check for collision with white ball
            for ball in other_balls:
                if isinstance(ball, WhiteBall):
                    if self.rect.colliderect(ball.rect):
                        self.on_track = False

        else:
            # Move the black ball away from the white ball
            super().update(other_balls)
            # check if black ball touches the track
            for point in self.track_points:
                buffer_rect = pygame.Rect(point[0]-5, point[1]-5, 15, 15)
                if self.rect.colliderect(buffer_rect):
                    self.on_track = True
                    # break the loop after the collision with one of the track points
                    break

    def draw_track(self, screen):
        # Draws the track based on the track points in self.track_points
        for i in range(len(self.track_points) - 1):
            pygame.draw.line(screen, (255, 0, 0), self.track_points[i], self.track_points[i + 1], 15)


class WhiteBall(MainBall):
    def __init__(self, x, y):
        super().__init__((0, 0, 255), x, y, 25, 5)
        print(f"WhiteBall rect: {self.rect}")

    def update(self, other_balls):
        super().update(other_balls)

        # Bounce of white balls when hit the black ball
        for ball in other_balls:
            if isinstance(ball, BlackBall) and ball != self and pygame.sprite.collide_circle(self, ball):
                self.direction = random.randint(0, 360)

        # Slow down over time
        # if self.speed > 0:
        #     self.speed -= 0.005
            # print("Current speed:", self.speed)
        # Stop the ball completely
        # elif self.speed <=0:
        #     self.speed = 0
