# projectile.py

import pygame
import random
from constants import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PROJECTILE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    @staticmethod
    def spawn():
        x = SCREEN_WIDTH
        y = random.randint(0, SCREEN_HEIGHT - PROJECTILE_HEIGHT)
        return Projectile(x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)

    def move(self):
        self.rect.x -= PROJECTILE_SPEED
        if self.rect.right < 0:
            self.kill()