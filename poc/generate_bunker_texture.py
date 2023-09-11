import pygame

SIZE = 800, 600

def tile_texture(texture, size):
    result = pygame.Surface(size, depth=32)
    for x in range(0, size[0], texture.get_width()):
        for y in range(0, size[1], texture.get_height()):
            result.blit(texture, (x, y))
    return result

def apply_alpha(texture, mask):
    texture = texture.convert_alpha()
    target = pygame.surfarray.pixels_alpha(texture)
    target[:] = pygame.surfarray.array2d(mask)
    del target
    return texture

def stamp(image, texture, mask):
    image.blit(apply_alpha(texture, mask), (0, 0))

def main():
    pygame.init()
    
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Textured Shield Example")
    
    texture = tile_texture(pygame.image.load("bunker_texture2.jpg"), SIZE)
    
    mask = pygame.Surface(SIZE, depth=8)
    width, height = SIZE
    shield_width = 125
    shield_height = 75
    bevel_height = 10
    points = [
        (width // 2 - shield_width // 2, height),
        (width // 2 + shield_width // 2, height),
        (width // 2 + shield_width // 2, height - shield_height),
        (width // 2 + shield_width // 2 - bevel_height, height - shield_height - bevel_height),
        (width // 2 - shield_width // 2 + bevel_height, height - shield_height - bevel_height),
        (width // 2 - shield_width // 2, height - shield_height),
    ]
    pygame.draw.polygon(mask, 255, points, 0)

    image = pygame.Surface(SIZE, pygame.SRCALPHA)
    stamp(image, texture, mask)
    
    pygame.image.save(image, "bunker.png")  # Save the image as PNG

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
