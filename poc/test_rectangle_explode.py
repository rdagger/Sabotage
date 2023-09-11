import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1024
screen_height = 1024


# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Exploding Rectangle")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
fps = 60

class FallingPiece(pygame.sprite.Sprite):
    def __init__(self, x, y, vertices, color):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, color, vertices)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-10, -5)
        self.rotation_angle = random.randint(0, 360)
        self.rotation_speed = self.speed_x * -1

    def update(self):
        self.rotation_angle += self.rotation_speed
        self.speed_y += 0.5  # Simulate gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top >= screen_height:
            self.kill()

    def draw_rotated(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect.topleft)



# Create the exploding rectangle
class ExplodingRectangle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill("darkkhaki")
        self.rect = self.image.get_rect(center=(x, y))
        self.explosion_time = pygame.time.get_ticks() + 3000  # 3 seconds
        self.exploded = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time >= self.explosion_time and not self.exploded:
            self.explode()
            self.exploded = True

    def explode(self):
        x, y = self.rect.center
        for _ in range(16):
            vertices = []
            for _ in range(random.randint(4, 8)):
                vertex = (random.randint(-20, 20), random.randint(-20, 20))
                vertices.append(vertex)

            colors = ["darkkhaki", "orange", "red"]
            weights = [0.65, 0.20, 0.15]

            color = random.choices(colors, weights=weights)[0]
                
            #color = random.choice([chartreuse, red, orange])
            falling_pieces.add(FallingPiece(x, y, vertices, color))

while True:
    # Create sprite group for falling pieces
    falling_pieces = pygame.sprite.Group()

    # Create the exploding rectangle in the center of the screen
    exploding_rect = ExplodingRectangle(screen_width // 2, screen_height // 4, 100, 25)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
            

        # Update the sprite groups
        exploding_rect.update()
        falling_pieces.update()

        # Clear the screen
        screen.fill("black")

        # Draw the exploding rectangle
        if not exploding_rect.exploded:
            screen.blit(exploding_rect.image, exploding_rect.rect)

        # Draw the falling pieces
        for piece in falling_pieces:
            piece.draw_rotated(screen)

        # Update the display
        pygame.display.update()

        # Limit the frame rate
        clock.tick(fps)

        if exploding_rect.exploded and not falling_pieces.sprites():
            break
