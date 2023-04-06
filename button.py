
import pygame

from setting import *



class Button:
    def __init__(self, y, text, bg_color):
        # self.image = pygame.image.load(image_path)
        # self.rect = self.image.get_rect()
        # self.rect.topleft = (screenwidth/2 - self.width/2, y - self.height/2)
        self.width = 200
        self.height = 50
        self.rect = pygame.Rect(screenwidth/2 - self.width/2, y - self.height/2, self.width, self.height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', 32)
        self.font_color = BLACK
        self.bg_color = bg_color

    def draw(self, surface):
        # surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
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
    
class BrightnessControl:
    def __init__(self):
        self.brightness = 255