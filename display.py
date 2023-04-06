import pygame
from setting import *
from button import Button, Volume
pygame.init()

screen = pygame.display.set_mode((screenwidth, screenheight))

# Set up the game clock
clock = pygame.time.Clock()

# Create checkbox rect and font
checkbox_rect = pygame.Rect(50, 50, 20, 20)
checkbox_font = pygame.font.SysFont(None, 24)
back_button = Button(520,"Back",WHITE)

# Run the game loop
game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
                if checkbox_rect.collidepoint(event.pos):
                    # Toggle full screen
                    if screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode((screenwidth, screenheight))
                    else:
                        pygame.display.set_mode((screenwidth, screenheight), pygame.FULLSCREEN)
                elif back_button.is_clicked(mouse_pos):
                    from option import *
                

    # Clear the screen
    screen.fill(WHITE)

    # Draw the checkbox
    pygame.draw.rect(screen, BLACK, checkbox_rect, 2)
    if screen.get_flags() & pygame.FULLSCREEN:
        pygame.draw.line(screen, BLACK, (checkbox_rect.left + 3, checkbox_rect.centery), (checkbox_rect.right - 3, checkbox_rect.centery), 3)
    back_button.draw(screen)
    # Draw the label
    label_text = "Full Screen"
    if screen.get_flags() & pygame.FULLSCREEN:
        label_text += " (ON)"
    else:
        label_text += " (OFF)"
    label_surface = checkbox_font.render(label_text, True, BLACK)
    label_rect = label_surface.get_rect(midleft=(checkbox_rect.right + 10, checkbox_rect.centery))
    screen.blit(label_surface, label_rect)

    # Update the display
    pygame.display.update()

    # Tick the clock to control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()