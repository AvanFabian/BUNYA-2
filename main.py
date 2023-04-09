import pygame
import random
from setting import *
from bola3 import BlackBall, WhiteBall, C, O, H
from elemenyer import Elemenyer, Score



# Define the character sprite class
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/charabunya.png").convert_alpha()  # Load the sprite image
        self.rect = self.image.get_rect()  # Use the image's rect as the sprite's rect
        self.rect.center = (x, y)
        self.speed = 10
        self.collision_box = self.image.get_rect()  # Use the sprite image's rect as the collision box
        self.collision_box.center = self.rect.center  # Position the collision box at the center of the sprite
        self.current_scale = 1.0  # Define a variable to keep track of the current scale of the image
        self.max_scale_factor = 1.1
        self.scale_speed = 0.001

        # Define a variable to keep track of whether the image is scaling up or down
        self.scaling_up = True

        # Set initial values for movement flags
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        # Load the character sprites for each direction
        self.character_images = dict(up="assets/charabunya.png", down="assets/charabunya.png", left="assets/charabunya.png", right="assets/charabunya.png",
                            default="assets/charabunya.png")


    # moving of the character
    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.collision_box.center = self.rect.center  # Update the position of the collision box to match the sprite
        # Check if the ball collides with the edges of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screenwidth:
            self.rect.right = screenwidth
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screenheight:
            self.rect.bottom = screenheight

    # display the character drawing
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # Updating image of character
    def update_image(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()

    # Movement of character
    def movement(self):
        if self.move_up:
            print("ke atas")
            self.update_image(self.character_images["up"])
            self.move(0, -1)
        elif self.move_down:
            print("ke bawah")
            self.update_image(self.character_images["down"])
            self.move(0, 1)
        elif self.move_right:
            print("ke kanan")
            self.update_image(self.character_images["right"])
            self.move(1, 0)
        elif self.move_left:
            print("ke kiri")
            self.update_image(self.character_images["left"])
            self.move(-1, 0)
        # update image for idle
        else:
            self.update_image(self.character_images["default"])

    # Handle the input from player
    def handle_event(self, event):
        # if button pressed
        if event.type == pygame.KEYDOWN:
            # Movement control
            if event.key == pygame.K_UP:
                self.move_up = True
            elif event.key == pygame.K_DOWN:
                self.move_down = True
            elif event.key == pygame.K_LEFT:
                self.move_left = True
            elif event.key == pygame.K_RIGHT:
                self.move_right = True
            elif event.key == pygame.K_SPACE:
                return 0
            elif event.key == pygame.K_x:
                kick = Kick(main.character, main.white_balls)
                kick.do_kick()

        # if button unpressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.move_up = False
            elif event.key == pygame.K_DOWN:
                self.move_down = False
            elif event.key == pygame.K_LEFT:
                self.move_left = False
            elif event.key == pygame.K_RIGHT:
                self.move_right = False

# Character kick feature
class Kick:
    def __init__(self, character, ball):
        self.character = character
        self.ball = ball

    def do_kick(self):
        for object in self.ball:
        # check if this is whiteball
            if isinstance(object, WhiteBall):
                if self.character.rect.colliderect(object.rect):
                    # print("Kick successful!")
                    object.direction = random.randint(0, 360)
                    object.speed += 5  # Increase the speed of ball by 5

#Lose condition
class LoseDetector(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, ballarrayinput, num_rows, num_columns):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.set_alpha(128)
        self.image.fill(RED)
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
                    if isinstance(sprite, BlackBall) and pygame.sprite.collide_rect(sprite, self):
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
        black_balls = [ball for ball in ballarray.sprites() if isinstance(ball, BlackBall)]
        for ball in black_balls:
            if pygame.sprite.collide_rect(self, ball):
                self.ballarray_colliding.append(ball)
                if ball not in self.ballarray:
                    self.ballarray.append(ball)
                    self.black_ball_counter += 1
                    # for ball_inside in self.ballarray:
                    #     if isinstance(ball_inside, BlackBall):
                    #         ballarray.remove(ball_inside)
                    #         ball_inside.kill()
                else:
                    if ball.rect.left < self.rect.left:
                        ball.rect.left = self.rect.left
                    elif ball.rect.right > self.rect.right:
                        ball.rect.right = self.rect.right
                    if ball.rect.top < self.rect.top:
                        ball.rect.top = self.rect.top
                    elif ball.rect.bottom > self.rect.bottom:
                        ball.rect.bottom = self.rect.bottom
        # Check for lose condition
        if len(self.ballarray_colliding) >= 10:
            return True

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 2)
class EndScreen:
    def __init__(self, score):
        pygame.init()

        self.game_display = pygame.display.set_mode((screenwidth, screenheight))
        pygame.display.set_caption("Bunya: Mari buat senyawa")

        # Set up the font for displaying text
        self.font = pygame.font.SysFont(None, 50)

        # Define the colors we'll use
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.score = score

    def run(self):
        game_over = True

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Clear the screen
            self.game_display.fill(self.white)

            # Draw the text for the game over message and the score
            message = self.font.render("Game Over", True, self.black)
            score_text = self.font.render("Score: " + str(self.score), True, self.black)
            message_rect = message.get_rect(center=(screenwidth/2, screenheight/3))
            score_rect = score_text.get_rect(center=(screenwidth/2, screenheight/2))
            self.game_display.blit(message, message_rect)
            self.game_display.blit(score_text, score_rect)

            # Draw the buttons
            back_button = pygame.draw.rect(self.game_display, self.black, (100, 450, 200, 50))
            replay_button = pygame.draw.rect(self.game_display, self.black, (500, 450, 200, 50))

            # Draw the text for the buttons
            back_text = self.font.render("Back", True, self.white)
            replay_text = self.font.render("Replay", True, self.white)
            back_text_rect = back_text.get_rect(center=back_button.center)
            replay_text_rect = replay_text.get_rect(center=replay_button.center)
            self.game_display.blit(back_text, back_text_rect)
            self.game_display.blit(replay_text, replay_text_rect)

            # Check for button clicks
            mouse_pos = pygame.mouse.get_pos()
            if back_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    # Handle back button click
                    print("Back button clicked")
                    game_over = False
            if replay_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    # Handle replay button click
                    print("Replay button clicked")
                    game_over = False

            # Update the screen
            pygame.display.update()

class Main:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.game_display = pygame.display.set_mode((screenwidth, screenheight))

        # Set the window title
        pygame.display.set_caption("Bunya: Mari buat senyawa")
        # Stage background
        self.background = pygame.image.load("assets/bg_stage.png").convert()

        # Set up the game clock
        self.clock = pygame.time.Clock()

        #score
        self.score = Score()

        # Character
        self.character = Character(screenwidth / 2, screenheight / 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.character)

        # Create the black balls
        self.black_balls = [BlackBall(random.random() * screenwidth, random.random() * screenheight, start_idx=i) for i in range(9)]
        # self.o_balls = [O(random.random() * screenwidth, random.random() * screenheight) for i in range(5)]
        # self.c_balls = [C(random.random() * screenwidth, random.random() * screenheight) for i in range(5)]
        # self.h_balls = [H(random.random() * screenwidth, random.random() * screenheight) for i in range(5)]
        # Add the balls to sprite groups
        # Create the white balls
        self.white_balls = [WhiteBall(random.random() * screenwidth, random.random() * screenheight) for i in range(1)]

        self.all_balls = pygame.sprite.Group()
        self.all_balls.add(self.white_balls)
        self.all_balls.add(self.black_balls)

        # Elemenyer
        self.elemenyer1 =  Elemenyer(0, screenheight*0.56, 100, 300, self.all_balls, 1, 3)
        self.elemenyer2 =  Elemenyer(screenwidth*0.41, 0 , 300, 100, self.all_balls, 1, 3)
        self.elemenyer_group = pygame.sprite.Group()
        self.elemenyer_group.add(self.elemenyer1)
        self.elemenyer_group.add(self.elemenyer2)

        #Lose Detector
        self.detector = LoseDetector(screenwidth*0.4, screenheight, 500, 100, self.all_balls, 1, 3)
        self.detector_group = pygame.sprite.Group()
        self.detector_group.add(self.detector)
    def run(self):
        # Set up the game loop
        main_run = True
        while main_run:
            # Handle events
            for event in pygame.event.get():
                # event when quit pressed
                if event.type == pygame.QUIT:
                    main_run = False
                # event when button pressed
                elif event:
                    self.character.handle_event(event)            

            # Update the balls
            self.all_balls.update(self.all_balls)
            # if len(self.all_balls) == 1:
            #     main_run = False

            # Execute Method
            self.character.update()
            self.character.movement()
            for elemenyer in self.elemenyer_group:
                elemenyer.update(self.all_balls, self.score)
            self.detector.update(self.all_balls)
            if self.detector.update(self.all_balls):
                main_run = False
            # Draw the game world
            # Scale the background image to fit the new surface
            self.game_display.blit(pygame.transform.scale(self.background, (screenwidth, screenheight)), (0, 0))
            self.all_balls.draw(self.game_display)  # Draw all ball
            self.character.draw(self.game_display)
            self.all_sprites.draw(self.game_display)  # Draw all sprites
            self.elemenyer1.draw(self.game_display)
            self.elemenyer2.draw(self.game_display)
            self.detector.draw(self.game_display)
            self.score.draw(self.game_display)

            if self.score.score >= 20:
                main_run = False
            
            pygame.display.flip()

            # Update the display
            pygame.display.update()

            # Tick the clock to control the frame rate
            self.clock.tick(60)
        end = EndScreen(self.score.score)
        end.run()

main = Main()
main.run()

