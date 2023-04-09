import pygame
import random
from setting import *
from bola3 import BlackBall, WhiteBall
from elemenyer import Elemenyer


# Define the character sprite class
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("HIDROGEN.png").convert_alpha()  # Load the sprite image
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
        self.character_images = dict(up="OKSIGEN.png", down="OKSIGEN.png", left="OKSIGEN.png", right="OKSIGEN.png",
                            default="HIDROGEN.png")


    # moving of the character
    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.collision_box.center = self.rect.center  # Update the position of the collision box to match the sprite

    # animation of the sprite
    # def animation(self):
    #     if self.scaling_up:
    #         self.current_scale += self.scale_speed
    #         if self.current_scale >= self.max_scale_factor:
    #             self.current_scale = self.max_scale_factor
    #             self.scaling_up = False
    #     else:
    #         self.current_scale -= self.scale_speed
    #         if self.current_scale <= 1.0:
    #             self.current_scale = 1.0
    #             self.scaling_up = True

    #     # Scale the image
    #     scaled_image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.current_scale), int(self.image.get_height() * self.current_scale)))

    #     # Center the scaled image on the screen
    #     self.image_pos = scaled_image.get_rect(center=self.image.get_rect(center=(pygame.display.get_surface().get_width()/2, pygame.display.get_surface().get_height()/2)).center)

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
            # Jump control
            elif event.key == pygame.K_SPACE:
                self.jump()
                # Kick control
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

                # Make character jump

    def jump(self):
        if not self.jump_flag:
            self.jump_flag = True
            self.rect.height += self.jump_size  # Increase the height of the character
            self.collision_box.height = self.rect.height  # Adjust the collision box
            self.jump_timer = 0

    # update the status of jump condition
    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screenwidth:
            self.rect.right = screenwidth
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screenheight:
            self.rect.bottom = screenheight
        if self.jump_flag:
            # Increase the jump timer
            self.jump_timer += 1
            # If the jump duration is over, disable the jump flag and reset the size of the character
            if self.jump_timer >= self.jump_duration:
                self.jump_flag = False
                self.rect.height -= self.jump_size
                self.collision_box.height = self.rect.height

    # method of detection collision
    def detect_collisions(self, surface):
        if self.jump_flag:  # Skip collision detection if the character is jumping
            print("loncat")
            return

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

class Main:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.game_display = pygame.display.set_mode((screenwidth, screenheight))

        # Set the window title
        pygame.display.set_caption("My Game")
        # Stage background
        self.background = pygame.image.load("bg_stage.png").convert()
        # Set up the game clock
        self.clock = pygame.time.Clock()


        # Character
        self.character = Character(screenwidth / 2, screenheight / 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.character)


        # Create the black balls
        self.black_balls = [BlackBall(50, 100), BlackBall(100, 150), BlackBall(80, 250), BlackBall(30, 200)]
        # black_balls = BlackBall(50, 50)

        # Create the white balls
        self.white_balls = [WhiteBall(random.random() * screenwidth, random.random() * screenheight) for i in range(1)]

        # Add the balls to sprite groups
        self.all_balls = pygame.sprite.Group()
        self.all_balls.add(self.black_balls)
        self.all_balls.add(self.white_balls)

        # Elemenyer
        self.elemenyer1 =  Elemenyer(0, screenheight*0.5, 100, 300, self.all_balls, 1, 3)
        self.elemenyer2 =  Elemenyer(screenwidth*0.5, 0 , 300, 100, self.all_balls, 1, 3)
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
            self.character.detect_collisions(self.game_display)
            self.character.update()
            self.character.movement()
            self.elemenyer1.update(self.all_balls)
            self.elemenyer2.update(self.all_balls)


            # Draw the game world
            # Scale the background image to fit the new surface
            self.game_display.blit(pygame.transform.scale(self.background, (screenwidth, screenheight)), (0, 0))
            self.all_balls.draw(self.game_display)  # Draw all ball
            self.character.draw(self.game_display)
            self.all_sprites.draw(self.game_display)  # Draw all sprites
            self.elemenyer1.draw(self.game_display)
            self.elemenyer2.draw(self.game_display)


            pygame.display.flip()

            # BlackBall.draw_track(game_display)
            # for ball in black_balls:
            # Update the display
            pygame.display.update()

            # Tick the clock to control the frame rate
            self.clock.tick(120)

        # Quit Pygame
        pygame.quit()

main = Main()
main.run()
