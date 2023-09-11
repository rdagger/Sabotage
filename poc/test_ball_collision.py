import pygame
import sys
from time import sleep

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

# Ball properties
ball_radius = 5
ball_initial_speed_x = -5
ball_initial_speed_y = -5

# Wall properties
wall_margin = 30
wall_thickness = 10

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
fps = 60

# Ball initial position and speed
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed = pygame.math.Vector2(ball_initial_speed_x, ball_initial_speed_y)

# Define the Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(green)
        self.rect = self.image.get_rect(topleft=(x, y))

# Create walls using sprite group
walls = pygame.sprite.Group()
top_wall = Wall(wall_margin, wall_margin - wall_thickness, screen_width - 2 * wall_margin, wall_thickness)
bottom_wall = Wall(wall_margin, screen_height - wall_margin, screen_width - 2 * wall_margin, wall_thickness)
left_wall = Wall(wall_margin - wall_thickness, wall_margin, wall_thickness, screen_height - 2 * wall_margin)
right_wall = Wall(screen_width - wall_margin, wall_margin, wall_thickness, screen_height - 2 * wall_margin)
walls.add(top_wall, bottom_wall, left_wall, right_wall)

# Create the ball sprite
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, speed):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, yellow, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.position = pygame.math.Vector2(x, y)  # Required to use fractional positions

    def update(self):
        # Calculate the next position of the ball
        next_x = self.position.x + self.speed.x
        next_y = self.position.y + self.speed.y
        # Caculate minimum increments
        x_inc, y_inc = self.speed.normalize()
        # The inc_count should be the same unless a speed is zero        
        if abs(x_inc) > abs(y_inc):
            inc_count = int(round(self.speed.x / x_inc, 0))
        else:
            inc_count = int(round(self.speed.y / y_inc, 0))
        # Store previous coordinates
        prev_x, prev_y = self.position.x, self.position.y
        #print(f"next_x: {next_x}, next_y: {next_y}, inc_count: {inc_count}, x_inc: {x_inc}, y_inc: {y_inc}")
        
        # Iterate through all position from current to next
        for _ in range(inc_count):
            self.position.x += x_inc
            self.position.y += y_inc

            # Skip if coordinates did not change
            if self.position.x == prev_x and self.position.y == prev_y:
                continue
            # Check for collision with walls (spritecollideany would only return first sprite hit)
            self.rect.x, self.rect.y = self.position.x, self.position.y
            wall_collisions = pygame.sprite.spritecollide(self, walls, False, pygame.sprite.collide_mask)
            if wall_collisions:
                # Back ball up to last non-colliding position
                self.position.x, self.position.y  = prev_x, prev_y
                self.rect.x, self.rect.y = self.position.x, self.position.y
                if top_wall in wall_collisions or bottom_wall in wall_collisions:
                    self.speed.y *= -1
                if left_wall in wall_collisions or right_wall in wall_collisions:
                    self.speed.x *= -1
                return
            prev_x, prev_y = self.position.x, self.position.y

# Create the ball
ball = Ball(ball_x, ball_y, ball_radius, ball_speed)

# Add the ball to a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(ball)
hit = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the ball sprite
    all_sprites.update()

    # Clear the screen
    screen.fill(black)

    # Draw the walls
    walls.draw(screen)

    # Draw the ball sprite
    all_sprites.draw(screen)

    # Update the display
    hit = pygame.display.update()

    # Limit the frame rate
    clock.tick(fps)
