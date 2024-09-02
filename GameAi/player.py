import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity_y = 0
        self.on_ground = False
        self.can_double_jump = False
        self.can_wall_jump = False
        self.can_dash = True
        self.dashing = False
        self.dash_time = 0

    def update(self):
        if not self.dashing:
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y

        # Check for collision with the ground
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True
            self.can_double_jump = True
            self.can_wall_jump = False
            self.can_dash = True
            # End the game if the player hits the floor


    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            self.can_double_jump = True
        elif self.can_double_jump:
            self.velocity_y = JUMP_STRENGTH
            self.can_double_jump = False
        elif self.can_wall_jump:
            self.velocity_y = JUMP_STRENGTH
            self.can_wall_jump = False

    def dash(self, direction):
        if self.can_dash:
            self.dashing = True
            self.dash_time = FPS // DASH_DURATION
            self.rect.x += DASH_SPEED * direction
            self.can_dash = False

    def reset_dash(self):
        self.dashing = False
