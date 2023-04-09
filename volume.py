# import pygame
# from button import Button
# from setting import *

# class Volume:
#     def __init__(self, initial_volume=0.5, min_volume=0.0, max_volume=1.0, step=0.1):
#         self.volume = initial_volume
#         self.min_volume = min_volume
#         self.max_volume = max_volume
#         self.step = step

#     def increase_volume(self):
#         self.volume = min(self.volume + self.step, self.max_volume)

#     def decrease_volume(self):
#         self.volume = max(self.volume - self.step, self.min_volume)

#     def set_volume(self, volume):
#         self.volume = max(min(volume, self.max_volume), self.min_volume)

#     def get_volume(self):
#         return self.volume

import pygame
from button import Button
from setting import *

class Volume:
    def __init__(self, initial_volume=0.5, min_volume=0.0, max_volume=1.0, step=0.1):
        self.volume = initial_volume
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.step = step

        pygame.init()

        self.screen = pygame.display.set_mode((screenwidth, screenheight))

        # Set up the game clock
        self.clock = pygame.time.Clock()

        # Create Volume objects
        self.music_volume = Volume(50, 100, 50,  "Music Volume")
        self.sfx_volume = Volume(150, 100, 50,  "SFX Volume")

        # Load sound files
        self.music = pygame.mixer.Sound("music.ogg")   # replace "music.ogg" with your music file name
        self.sfx = pygame.mixer.Sound("sfx.ogg")       # replace "sfx.ogg" with your sound effects file name

        # Set initial volume levels (0.0 to 1.0)
        self.music_volume.set_level(0.5)
        self.sfx_volume.set_level(0.7)
        self.music.set_volume(self.music_volume.get_level())
        self.sfx.set_volume(self.sfx_volume.get_level())

        #initialize button
        self.back_button = Button(620,"BACK",WHITE)


    def run(self):
        volume_run = True
        while volume_run:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    volume_run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # get mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    if self.music_volume.is_clicked(mouse_pos):
                        self.music_volume.adjust_level()
                        self.music.set_volume(self.music_volume.get_level())
                    elif self.sfx_volume.is_clicked(mouse_pos):
                        self.sfx_volume.adjust_level()
                        self.sfx.set_volume(self.sfx_volume.get_level())
                    elif self.back_button.is_clicked(mouse_pos):
                        volume_run = False 

            self.screen.fill(BLACK)

            # Draw Volume objects
            self.music_volume.draw(self.screen)
            self.sfx_volume.draw(self.screen)
            self.back_button.draw(self.screen)

            # Update the display
            pygame.display.update()

            # Tick the clock to control the frame rate
            self.clock.tick(120)

        # Quit Pygame
        pygame.quit()
volume = Volume
volume.run()
