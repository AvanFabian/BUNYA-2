import pygame
from setting import *
from volume import *

pygame.init()


class Volume:
    def __init__(self, initial_volume=0.5, min_volume=0.0, max_volume=1.0, step=0.1):
        self.volume = initial_volume
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.step = step

    def increase_volume(self):
        self.volume = min(self.volume + self.step, self.max_volume)

    def decrease_volume(self):
        self.volume = max(self.volume - self.step, self.min_volume)

    def set_volume(self, volume):
        self.volume = max(min(volume, self.max_volume), self.min_volume)

    def get_volume(self):
        return self.volume



screen = pygame.display.set_mode((screenwidth, screenheight))

# Set up the game clock
clock = pygame.time.Clock()

# Create Volume objects
music_volume = Volume(50, 100, 50,  "Music Volume")
sfx_volume = Volume(150, 100, 50,  "SFX Volume")

# Load sound files
music = pygame.mixer.Sound("music.ogg")   # replace "music.ogg" with your music file name
sfx = pygame.mixer.Sound("sfx.ogg")       # replace "sfx.ogg" with your sound effects file name

# Set initial volume levels (0.0 to 1.0)
music_volume.set_level(0.5)
sfx_volume.set_level(0.7)
music.set_volume(music_volume.get_level())
sfx.set_volume(sfx_volume.get_level())

game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get mouse position
            volume_mouse_pos = pygame.mouse.get_pos()
            if music_volume.is_clicked(volume_mouse_pos):
                music_volume.adjust_level()
                music.set_volume(music_volume.get_level())
            elif sfx_volume.is_clicked(volume_mouse_pos):
                sfx_volume.adjust_level()
                sfx.set_volume(sfx_volume.get_level())

    screen.fill(BLACK)

    # Draw Volume objects
    music_volume.draw(screen)
    sfx_volume.draw(screen)

    # Update the display
    pygame.display.update()

    # Tick the clock to control the frame rate
    clock.tick(120)

# Quit Pygame
pygame.quit()
