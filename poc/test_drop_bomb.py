import pygame
import random

# Initialize pygame
pygame.init()

# Window dimensions
WIDTH = 1024
HEIGHT = 1024

TRAJECTORY = {
    2: 40,
    3: 80,
    4: 125,
    5: 175,
    6: 225,
    7: 275,
}

# Colors
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

# Define screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define objects
plane = pygame.Rect(0, 0, 59, 51)
bunker = pygame.Rect(WIDTH // 2 - 97 // 2, HEIGHT - 85, 97, 85)

gravity = 0.08
bomb_speed_y = 0
plane_speed = 0


# Load bomb sprite
bomb_image = pygame.image.load('bomb.png').convert_alpha()
bomb_rect = bomb_image.get_rect()

def reset_plane():
    global plane_speed, plane_direction, bomb_dropped, bomb_speed_y, bomb_speed_x, bomb_angle
    plane_speed = random.randint(3, 7)
    plane_direction = 1 if random.choice([True, False]) else -1
    plane.top = random.choice([70, 140, 210, 280, 350])  # random heights
    plane.left = 0 if plane_direction == 1 else WIDTH
    bomb_dropped = False
    bomb_speed_y = 0
    bomb_speed_x = plane_direction * plane_speed
    bomb_angle = 90 if plane_direction == 1 else -90

reset_plane()

bomb_hit = False

# Game loop
running = True
while running:
    screen.fill("skyblue4")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Plane movement
    plane.move_ip(plane_direction * plane_speed, 0)

    if bomb_hit and (plane.left > WIDTH or plane.right < 0):
        reset_plane()
        bomb_hit = False

    # Decide when to drop bomb
    if not bomb_dropped: #and (WIDTH // 4 < plane.centerx < 3 * WIDTH // 4):
        target_x = random.randint(bunker.left + 10, bunker.right - 10)
        
        if plane_direction == 1 and plane.centerx > target_x - (TRAJECTORY[abs(plane_speed)]):
            bomb_dropped = True
        elif plane_direction == -1 and plane.centerx < target_x + (TRAJECTORY[abs(plane_speed)]):
            bomb_dropped = True

        if bomb_dropped:
            bomb_rect.midtop = plane.midbottom

    # Bomb physics
    if bomb_dropped:
        bomb_speed_y += gravity
        bomb_rect.move_ip(bomb_speed_x, bomb_speed_y)

        # Adjust bomb angle downwards during fall
        if (plane_direction == 1 and bomb_angle > 0) or (plane_direction == -1 and bomb_angle < 0):
            bomb_angle += (-plane_direction)

        
        # Reduce x speed
        bomb_speed_x *= 0.981

        rotated_bomb = pygame.transform.rotate(bomb_image, bomb_angle)
        rotated_rect = rotated_bomb.get_rect(center=bomb_rect.center)

        # Ensure bomb doesn't move through bunker
        if rotated_rect.colliderect(bunker) and bomb_speed_y >= 0:
            rotated_rect.bottom = bunker.top
            bomb_speed_y = 0
            bomb_speed_x = 0
            bomb_hit = True

        if bomb_rect.bottom > 1024:
            bomb_hit = True

        # Draw bomb
        screen.blit(rotated_bomb, rotated_rect.topleft)

    pygame.draw.rect(screen, BLUE, plane)
    pygame.draw.rect(screen, GREY, bunker)
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
