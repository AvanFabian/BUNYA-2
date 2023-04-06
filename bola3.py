import random
import math
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


class BlackBall(MainBall):
    def __init__(self, x, y):
        super().__init__((0, 0, 0), x, y, 25, 5)
        self.start_direction = self.direction

        # Define the track of the black ball
        # Last index of track_points is the final point of the track
        self.track_points = [(screenwidth / 3.0, screenheight), (screenwidth / 3.0, 0)]

        self.track_idx = 0
        self.track_dir = 1
        # Create a rect to represent the black ball's position on the track
        self.track_rect = pygame.Rect(0, 0, 2 * self.radius, 2 * self.radius)
        # self.track_rect = pygame.Rect(*self.track_points[0], 20, 20)

    # Update method to move the black ball along the track from start to finish nad appearing again at the start and continuesly
    # Update the black ball's position on the track
    def update(self, other_balls):
        super().update(other_balls, self.track_rect)

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
        speed = 2
        if distance < speed:
            self.track_idx += self.track_dir
            self.track_rect.center = self.track_points[self.track_idx]
        else:
            self.track_rect.centerx += speed * math.cos(math.radians(angle))
            self.track_rect.centery += speed * math.sin(math.radians(angle))

        # Update the black ball's direction
        if self.track_idx == 0:
            self.direction = 180 - self.start_direction
        elif self.track_idx == len(self.track_points) - 1:
            self.direction = 360 - self.start_direction

        # Update the black ball's position
        self.rect.center = self.track_rect.center

        # Update the black ball's movement direction
        super().update(other_balls)

    def draw_track(self, screen):
        # Draws the track based on the track points in self.track_points
        for i in range(len(self.track_points) - 1):
            pygame.draw.line(screen, (255, 0, 0), self.track_points[i], self.track_points[i + 1], 15)


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

        # Slow down over time
        if self.speed > 0:
            self.speed -= 0.005
            # print("Current speed:", self.speed)
        # Stop the ball completely
        elif self.speed <=0:
            self.speed = 0

    # def update(self, other_balls):
    #     super().update(other_balls)

    #     # Bounce off walls
    #     if self.rect.left < 0 or self.rect.right > screenwidth:
    #         self.direction = 180 - self.direction
    #     if self.rect.top < 0 or self.rect.bottom > screenheight:
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
#         if self.rect.left < 0 or self.rect.right > screenwidth:
#             self.direction = 180 - self.start_direction
#         if self.rect.top < 0 or self.rect.bottom > screenheight:
#             self.direction = 360 - self.start_direction

# class WhiteBall(MainBall):
#     def __init__(self, x, y):
#         super().__init__((0, 0, 255), x, y, 10, 5)

#     def update(self, other_balls):
#         super().update(other_balls)

#         # Bounce off walls
#         if self.rect.left < 0 or self.rect.right > screenwidth:
#             self.direction = 180 - self.direction
#         if self.rect.top < 0 or self.rect.bottom > screenheight:
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
#     if self.rect.left < 0 or self.rect.right > screenwidth:
#         self.direction = 180 - self.direction
#     if self.rect.top < 0 or self.rect.bottom > screenheight:
#         self.direction = 360 - self.direction

#     # Check if the ball hit another ball
#     for ball in other_balls:
#         if self != ball and pygame.sprite.collide_circle(self, ball):
#             self.direction = random.randint(0, 360)


# # Update the position of the black ball
# if self.track_idx == len(self.track_points) - 1:
#     self.rect.left = -self.radius
# Update the position of the black ball


# other BLACKBALL SOlution # HARUS DI CEK JUGA!
# def update(self, all_balls):
#     super().update(other_balls=all_balls)

#     # Calculate the angle between the BlackBall's current position and the next point in the track
#     dx = self.track_points[self.track_idx+1][0] - self.track_rect.centerx
#     dy = self.track_points[self.track_idx+1][1] - self.track_rect.centery
#     target_angle = math.degrees(math.atan2(-dy, dx))

#     # Adjust the BlackBall's direction to move towards the next point in the track
#     angle_diff = (target_angle - self.direction + 180) % 360 - 180
#     if angle_diff < 0:
#         self.direction -= min(self.turn_speed, abs(angle_diff))
#     else:
#         self.direction += min(self.turn_speed, abs(angle_diff))

#     # Calculate the BlackBall's movement using its direction and speed
#     dx = math.cos(math.radians(self.direction)) * self.speed
#     dy = -math.sin(math.radians(self.direction)) * self.speed
#     dx = abs(dx) * self.track_dir  # Make sure dx is always positive

#     # Move the BlackBall based on its calculated movement
#     self.track_rect.move_ip(dx, dy)

#     # Check if the BlackBall has reached the next point in the track
#     if self.track_dir == 1:
#         if self.track_rect.bottom < self.track_points[self.track_idx+1][1]:
#             self.track_idx += 1
#     else:
#         if self.track_rect.top > self.track_points[self.track_idx+1][1]:
#             self.track_idx += 1

#     # Handle bouncing off track ends
#     if self.track_idx == len(self.track_points) - 1:
#         self.track_rect.topleft = (screenwidth/3.0, screenheight) # reset to start of track
#         self.track_idx = 0
#     elif self.track_idx == 0 and self.track_dir == -1:
#         self.track_dir = 1

#     # Adjust the ball's position based on the position of the track rectangle
#     self.rect.centerx = self.track_rect.centerx
#     self.rect.centery = self.track_rect.centery

#     # Update the direction of the black ball
#     if self.rect.left < 0 or self.rect.right > screenwidth:
#         self.direction = 180 - self.start_direction
#     if self.rect.top < 0:
#         self.direction = 360 - self.start_direction
#     if self.rect.bottom > screenheight:
#         self.direction = 180 - self.start_direction


# Backu method update lama dari BlackBall
# def update(self, all_balls):
#         super().update(other_balls=all_balls)

#         # Calculate the angle between the BlackBall's current position and the next point in the track
#         dx = self.track_points[self.track_idx+1][0] - self.track_rect.centerx
#         dy = self.track_points[self.track_idx+1][1] - self.track_rect.centery
#         target_angle = math.degrees(math.atan2(-dy, dx))
#         print(f"Target angle: {target_angle}")

#         # Adjust the BlackBall's direction to move towards the next point in the track
#         angle_diff = (target_angle - self.direction + 180) % 360 - 180
#         if angle_diff < 0:
#             self.direction -= min(self.speed, abs(angle_diff))
#         else:
#             self.direction += min(self.speed, abs(angle_diff))

#         # Move the BlackBall based on its direction and speed
#         dx = math.cos(math.radians(self.direction)) * self.speed
#         dy = -math.sin(math.radians(self.direction)) * self.speed
#         print(f"dx before IP : {dx} dy before IP : {dy}")
#         self.track_rect.move_ip(dx, dy)
#         print(f"dx after IP : {dx} dy after IP : {dy}")
#         print(f"Move IP : {self.track_rect.move_ip(dx, dy)}")

#         # Check if the BlackBall has passed the next point in the track
#         if self.track_dir == 1:
#             if self.track_rect.top > self.track_points[self.track_idx+1][1]:
#                 self.track_idx += 1
#         else:
#             if self.track_rect.bottom < self.track_points[self.track_idx+1][1]:
#                 self.track_idx += 1

#         # Handle bouncing off track ends
#         if self.track_idx == len(self.track_points) - 1:
#             self.track_rect.topleft = (screenwidth/3.0, screenheight) # reset to start of track
#             self.track_idx = 0
#         elif self.track_idx == 0 and self.track_dir == -1:
#             self.track_dir = 1

#         # Adjust the ball's position based on the position of the track rectangle
#         self.rect.centerx = self.track_rect.centerx
#         self.rect.centery = self.track_rect.centery

#         # Update the direction of the black ball
#         if self.rect.left < 0 or self.rect.right > screenwidth:
#             self.direction = 180 - self.start_direction
#         if self.rect.top < 0:
#             self.direction = 360 - self.start_direction
#         if self.rect.bottom > screenheight:
#             self.direction = 180 - self.start_direction

# def draw_track(self, screen):
#     # Draws the track based on the track points in self.track_points
#     for i in range(len(self.track_points) - 1):
#         pygame.draw.line(screen, (255, 0, 0), self.track_points[i], self.track_points[i+1], 15)
