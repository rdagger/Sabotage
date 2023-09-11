import pygame
import random

# Initialize pygame
pygame.init()

# Dimensions of each individual sprite and texture
SPRITE_WIDTH = 25
SPRITE_HEIGHT = 25
TEXTURE_WIDTH = 57
TEXTURE_HEIGHT = 57

# Load the texture
texture = pygame.image.load("texture_jet.png")

def generate_random_polygon(max_width, max_height):
    num_vertices = random.randint(3, 5)
    vertices = []

    for _ in range(num_vertices):
        px = random.randint(0, max_width)
        py = random.randint(0, max_height)
        vertices.append((px, py))

    return vertices

def draw_textured_polygon(surface, texture, points):
    polygon_surface = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT), pygame.SRCALPHA)

    # Draw a white polygon on an initially transparent surface
    pygame.draw.polygon(polygon_surface, (255, 255, 255, 255), points)

    # Choose a random starting point within the texture
    start_x = random.randint(0, TEXTURE_WIDTH - SPRITE_WIDTH)
    start_y = random.randint(0, TEXTURE_HEIGHT - SPRITE_HEIGHT)

    # Apply the texture based on the random starting point
    for px in range(SPRITE_WIDTH):
        for py in range(SPRITE_HEIGHT):
            if polygon_surface.get_at((px, py))[3] > 0:  # check the alpha value
                tx = (px + start_x) % TEXTURE_WIDTH
                ty = (py + start_y) % TEXTURE_HEIGHT
                polygon_surface.set_at((px, py), texture.get_at((tx, ty)))

    # Blit the textured polygon onto the provided surface
    surface.blit(polygon_surface, (0, 0))

# Create a surface for the sprite sheet with the SRCALPHA flag for transparency
sprite_sheet = pygame.Surface((64 * SPRITE_WIDTH, SPRITE_HEIGHT), pygame.SRCALPHA)

# Generate and draw the polygons to the sprite sheet
for i in range(64):
    polygon = generate_random_polygon(SPRITE_WIDTH, SPRITE_HEIGHT)
    temp_surface = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT), pygame.SRCALPHA)
    draw_textured_polygon(temp_surface, texture, polygon)
    sprite_sheet.blit(temp_surface, (i * SPRITE_WIDTH, 0))

# Save the sprite sheet to a file
pygame.image.save(sprite_sheet, "sprite_sheet.png")

pygame.quit()
