import pygame

class EndScreen:
    def __init__(self, score):
        pygame.init()

        # Set up the display window
        self.display_width = 800
        self.display_height = 600
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Game Over")

        # Set up the font for displaying text
        self.font = pygame.font.SysFont(None, 50)

        # Define the colors we'll use
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.score = score

    def show(self):
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

        # Quit the game
        pygame.quit()
        quit()
