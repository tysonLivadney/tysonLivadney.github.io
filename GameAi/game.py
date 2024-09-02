# game.py

import pygame
import sys
from constants import *
from player import Player
from platform import Platform
from projectile import Projectile

class Game:
    second_starting_platform = None
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 50)
        self.start_time = pygame.time.get_ticks()  # Start the timer
        self.reset()

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Convert to seconds
        timer_text = self.font.render(f"Time: {elapsed_time:.2f}", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))

    def reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        starting_platform = Platform(self.player.rect.x - PLATFORM_WIDTH // 2, self.player.rect.bottom, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.platforms.add(starting_platform)
        self.all_sprites.add(starting_platform)

        second_starting_platform = Platform(starting_platform.rect.x + 300, starting_platform.rect.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.platforms.add(second_starting_platform)
        self.all_sprites.add(second_starting_platform)

        self.last_spawn_time = 0
        self.last_projectile_spawn_time = pygame.time.get_ticks()
        self.last_platform_y = starting_platform.rect.y
        self.platform_speed = 1 #starting value
        self.start_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_LSHIFT:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        self.player.dash(-1)
                    elif keys[pygame.K_RIGHT]:
                        self.player.dash(1)
        return True

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += PLAYER_SPEED

        if not self.handle_collisions():
            return False

        self.spawn_platforms()
        self.spawn_projectiles()
        self.move_objects()

        self.all_sprites.update()
        return True

    def handle_collisions(self):
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > SCREEN_WIDTH:
            self.player.rect.right = SCREEN_WIDTH

        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in hits:
            if self.player.rect.right > platform.rect.left and self.player.rect.left < platform.rect.right:
                if self.player.rect.left < platform.rect.right and self.player.rect.right > platform.rect.right:
                    self.player.rect.left = platform.rect.right
                    self.player.can_wall_jump = True
                    self.player.can_dash = True
                elif self.player.rect.right > platform.rect.left and self.player.rect.left < platform.rect.left:
                    self.player.rect.right = platform.rect.left
                    self.player.can_wall_jump = True
                    self.player.can_dash = True

        self.player.update()
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in hits:
            if self.player.velocity_y > 0:
                self.player.rect.bottom = platform.rect.top
                self.player.velocity_y = 0
                self.player.on_ground = True
                self.player.can_double_jump = True
                self.player.can_wall_jump = False
                self.player.can_dash = True
            elif self.player.velocity_y < 0:
                self.player.rect.top = platform.rect.bottom
                self.player.velocity_y = 0

        if self.player.dashing:
            self.player.dash_time -= 1
            if self.player.dash_time <= 0:
                self.player.reset_dash()

        if pygame.sprite.spritecollide(self.player, self.projectiles, False):
            return False

        return True

    def spawn_platforms(self):
        current_time = pygame.time.get_ticks()
        
        if self.last_platform_y is None:
            self.last_platform_y = self.second_starting_platform.rect.y

        new_platform = Platform.spawn(self.last_platform_y, self.platform_speed, self.last_spawn_time)
        if new_platform:
            self.platforms.add(new_platform)
            self.all_sprites.add(new_platform)
            self.last_platform_y = new_platform.rect.y
            self.last_spawn_time = current_time

            # Increase speed, but keep it within limits
            if self.platform_speed + .12 <= MAX_PLATFORM_SPEED:
                self.platform_speed += .12

    def spawn_projectiles(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_projectile_spawn_time > 500:
            new_projectile = Projectile.spawn()
            self.projectiles.add(new_projectile)
            self.all_sprites.add(new_projectile)
            self.last_projectile_spawn_time = current_time

    def move_objects(self):
        for platform in self.platforms:
            platform.move(self.platform_speed)
        for projectile in self.projectiles:
            projectile.move()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.update_timer()
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            if self.update():
                self.draw()
                self.update_timer()
            else:
                running = False
        pygame.quit()

    def get_state(self):
        
        pass

    def step(self, action):
        if self.update():
            self.draw()
        pass

if __name__ == "__main__":
    game = Game()
    game.run()