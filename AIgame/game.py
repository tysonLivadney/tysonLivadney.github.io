import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (135, 206, 235)  # Light blue background
WHITE = (255, 255, 255)
FPS = 60

# Player constants
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 35
PLAYER_COLOR = (255, 0, 0)  # Red
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLAYER_SPEED = 5
DASH_SPEED = 60
DASH_DURATION = 6  # lower = longer
WALL_JUMP_STRENGTH = -10

# Platform constants
PLATFORM_COLOR = (0, 255, 0)  # Green
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 20
PLATFORM_SPEED = 1.5
MAX_PLATFORM_SPEED = 20

# Projectile constants
PROJECTILE_COLOR = (255, 0, 0)  # Red
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 20, 20
PROJECTILE_SPEED = 7

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Platformer')
clock = pygame.time.Clock()

# Player class
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
            print("Game Over")
            pygame.quit()
            sys.exit()

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
            self.handle_dash_collision()

    def reset_dash(self):
        self.dashing = False

    def handle_dash_collision(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if direction > 0:  # Dashing right
                self.rect.right = platform.rect.left
            elif direction < 0:  # Dashing left
                self.rect.left = platform.rect.right
            self.reset_dash()

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    @staticmethod
    def spawn(last_platform_y):
        x = SCREEN_WIDTH
        y = last_platform_y + random.choice([-100, 100])
        y = max(200, min(y, SCREEN_HEIGHT - PLATFORM_HEIGHT))
        platform = Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platforms.add(platform)
        all_sprites.add(platform)
        return y

    def move(self):
        self.rect.x -= PLATFORM_SPEED
        if self.rect.right < 0:
            self.kill()

# Projectile class
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
        projectile = Projectile(x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
        projectiles.add(projectile)
        all_sprites.add(projectile)

    def move(self):
        self.rect.x -= PROJECTILE_SPEED
        if self.rect.right < 0:
            self.kill()

# Create player and platform instances
player = Player()

# Sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Create a starting platform beneath the player
starting_platform = Platform(player.rect.x - PLATFORM_WIDTH // 2, player.rect.bottom, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platforms.add(starting_platform)
all_sprites.add(starting_platform)

# Create a second starting platform 300 to the right
second_starting_platform = Platform(starting_platform.rect.x + 300, starting_platform.rect.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platforms.add(second_starting_platform)
all_sprites.add(second_starting_platform)

# Add player to all_sprites
all_sprites.add(player)

# Game loop
last_spawn_time = pygame.time.get_ticks()
last_projectile_spawn_time = pygame.time.get_ticks()
last_platform_y = starting_platform.rect.y
platform_speed = PLATFORM_SPEED
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_LSHIFT:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    direction = -1
                    player.dash(direction)
                elif keys[pygame.K_RIGHT]:
                    direction = 1
                    player.dash(direction)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.rect.x += PLAYER_SPEED

    # Wall collision detection
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH

    # Horizontal collision detection
    hits = pygame.sprite.spritecollide(player, platforms, False)
    for platform in hits:
        if player.rect.right > platform.rect.left and player.rect.left < platform.rect.right:
            if player.rect.left < platform.rect.right and player.rect.right > platform.rect.right:
                player.rect.left = platform.rect.right
                player.can_wall_jump = True
                player.can_dash = True
            elif player.rect.right > platform.rect.left and player.rect.left < platform.rect.left:
                player.rect.right = platform.rect.left
                player.can_wall_jump = True
                player.can_dash = True

    # Vertical movement and collision detection
    player.update()
    hits = pygame.sprite.spritecollide(player, platforms, False)
    for platform in hits:
        if player.velocity_y > 0:  # Falling down
            player.rect.bottom = platform.rect.top
            player.velocity_y = 0
            player.on_ground = True
            player.can_double_jump = True
            player.can_wall_jump = False
            player.can_dash = True
        elif player.velocity_y < 0:  # Jumping up
            player.rect.top = platform.rect.bottom
            player.velocity_y = 0

    # Dash handling
    if player.dashing:
        player.dash_time -= 1
        if player.dash_time <= 0:
            player.reset_dash()

    # Spawn new platform every 3 seconds
    current_time = pygame.time.get_ticks()
    time_to_cross_screen = SCREEN_WIDTH / PLATFORM_SPEED
    spawn_interval = time_to_cross_screen * 6  # Adjust this multiplier as needed
    last_spawn_time = spawn_interval + 1
    
    if current_time - last_spawn_time > spawn_interval:
        last_platform_y = Platform.spawn(last_platform_y)
        last_spawn_time = current_time
        if platform_speed + 0.1 >= MAX_PLATFORM_SPEED: PLATFORM_SPEED += 0.1  # Increase platform speed
        time_to_cross_screen = SCREEN_WIDTH / PLATFORM_SPEED

    # Spawn new projectile every 3 seconds
    if current_time - last_projectile_spawn_time > 500:
        Projectile.spawn()
        last_projectile_spawn_time = current_time

    # Move platforms
    for platform in platforms:
        platform.move()

    # Move projectiles
    for projectile in projectiles:
        projectile.move()

    # Check for projectile collision with player
    if pygame.sprite.spritecollide(player, projectiles, False):
        print("Game Over")
        running = False

    # Draw
    screen.fill(BG_COLOR)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
