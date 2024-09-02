# platform.py

import pygame
import random
from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    @staticmethod
    def spawn(last_platform_y, platform_speed, last_spawn_time):
        distance_between_platforms = 200  # Set to an appropriate value based on your game
        spawn_interval = distance_between_platforms / platform_speed * 20 

        if pygame.time.get_ticks() - last_spawn_time > spawn_interval:
            x = SCREEN_WIDTH
            y = last_platform_y + random.choice([-100, 100])
            y = max(200, min(y, SCREEN_HEIGHT - PLATFORM_HEIGHT))
            return Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        return None


    def move(self, platform_speed):
        self.rect.x -= platform_speed
        if self.rect.right < 0:
            self.kill()