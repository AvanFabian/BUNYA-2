import pygame
import random
from setting import *
from bola3 import BlackBall, WhiteBall
from elemenyer import Elemenyer, Score



# Define the character sprite class
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/HIDROGEN.png").convert_alpha()  # Load the sprite image
        self.rect = self.image.get_rect()  # Use the image's rect as the sprite's rect
        self.rect.center = (x, y)
        self.speed = 5
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

        # initial jump method
        self.jump_size = 50  # Increase in height when jumping
        self.jump_duration = 30  # Duration of jump in frames
        self.jump_timer = 0  # Timer for tracking jump duration
        self.jump_flag = False  # Flag to indicate whether the character is jumping

        # Load the character sprites for each direction
        self.character_images = dict(up="assets/OKSIGEN.png", down="assets/OKSIGEN.png", left="assets/OKSIGEN.png", right="assets/OKSIGEN.png",
                            default="assets/HIDROGEN.png")


    # moving of the character
    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.collision_box.center = self.rect.center  # Update the position of the collision box to match the sprite

    # display the character drawing
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.collision_box, 2)
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

        # Set up the game clock
        self.clock = pygame.time.Clock()

        #score
        self.score = Score()

        # Character 
        self.character = Character(screenwidth / 2, screenheight / 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.character)


        # Create the black balls
        self.black_balls = [BlackBall(random.random() * screenwidth, random.random() * screenheight) for i in range(10)]
        # black_balls = BlackBall(50, 50)

        # Create the white balls
        self.white_balls = [WhiteBall(random.random() * screenwidth, random.random() * screenheight) for i in range(1)]

# Add the balls to sprite groups
all_balls = pygame.sprite.Group()
all_balls.add(black_balls)
all_balls.add(white_balls)

        # Elemenyer
        self.elemenyer1 =  Elemenyer(0, screenheight*0.56, 100, 300, self.all_balls, 1, 3)
        self.elemenyer2 =  Elemenyer(screenwidth*0.41, 0 , 300, 100, self.all_balls, 1, 3)
        self.elemenyer_group = pygame.sprite.Group()
        self.elemenyer_group.add(self.elemenyer1)
        self.elemenyer_group.add(self.elemenyer2)

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

            # Execute Method
            self.character.update()
            self.character.movement()
            for elemenyer in self.elemenyer_group:
                elemenyer.update(self.all_balls, self.score)

            # Draw the game world
            # Scale the background image to fit the new surface
            self.game_display.blit(pygame.transform.scale(self.background, (screenwidth, screenheight)), (0, 0))
            self.all_balls.draw(self.game_display)  # Draw all ball
            self.character.draw(self.game_display)
            self.all_sprites.draw(self.game_display)  # Draw all sprites
            self.elemenyer1.draw(self.game_display)
            self.elemenyer2.draw(self.game_display)
            self.score.draw(self.game_display)
            
            pygame.display.flip()

            # Update the display
            pygame.display.update()

            # Tick the clock to control the frame rate
            self.clock.tick(60)

main = Main()
main.run()

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
            message_rect = message.get_rect(center=(self.display_width/2, self.display_height/3))
            score_rect = score_text.get_rect(center=(self.display_width/2, self.display_height/2))
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
