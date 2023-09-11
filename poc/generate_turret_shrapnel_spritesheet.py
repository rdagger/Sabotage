import pygame
import random

# Initialize pygame
pygame.init()

# Dimensions of each individual sprite and texture
SPRITE_WIDTH = 25
SPRITE_HEIGHT = 25
SPRITE_PIECE_WIDTH = 8
SPRITE_PIECE_HEIGHT = 8
TEXTURE_WIDTH = 33
TEXTURE_HEIGHT = 31

# Load the texture
texture = pygame.image.load("texture_turret.png")

def generate_random_polygon(max_width, max_height):
    num_vertices = random.randint(3, 5)
    vertices = []

    for _ in range(num_vertices):
        px = random.randint(0, max_width - 1)
        py = random.randint(0, max_height - 1)
        vertices.append((px, py))

    return vertices

def draw_textured_polygon(surface, texture, points):
    min_x = min(points, key=lambda p: p[0])[0]
    min_y = min(points, key=lambda p: p[1])[1]

    polygon_surface = pygame.Surface((SPRITE_PIECE_WIDTH, SPRITE_PIECE_HEIGHT), pygame.SRCALPHA)

    pygame.draw.polygon(polygon_surface, (255, 255, 255, 255), [(x - min_x, y - min_y) for x, y in points])

    for px in range(SPRITE_PIECE_WIDTH):
        for py in range(SPRITE_PIECE_HEIGHT):
            if polygon_surface.get_at((px, py))[3] > 0:
                tx = (px + min_x) % TEXTURE_WIDTH
                ty = (py + min_y) % TEXTURE_HEIGHT
                polygon_surface.set_at((px, py), texture.get_at((tx, ty)))

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
