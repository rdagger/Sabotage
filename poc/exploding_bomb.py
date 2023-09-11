import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 1024

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("bomb Explosion")

# Load the images
bomb = pygame.image.load("bomb.png")
sprite_sheet = pygame.image.load("explosion_bomb.png")

# Colors
BLACK = (0, 0, 0)


class ExplodingPiece:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.y_velocity = random.uniform(-5, 0)
        self.x_velocity = random.uniform(-3, 3)
        self.angle = 0
        self.angular_velocity = random.uniform(-5, 5)

    def update(self):
        self.y_velocity += 0.2  # gravity effect
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.angle += self.angular_velocity

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect()
        rect.center = (self.x, self.y)
        surface.blit(rotated_image, rect.topleft)

    def off_screen(self):
        return self.y > HEIGHT

def get_sprite(idx):
    x = idx * 12
    return sprite_sheet.subsurface(pygame.Rect(x, 0, 12, 12))

clock = pygame.time.Clock()
exploding_pieces = []
reset_time = 2000
last_explode_time = None

running = True
while running:
    screen.fill("deepskyblue")

    if last_explode_time and pygame.time.get_ticks() - last_explode_time >= reset_time:
        exploding_pieces = []
        last_explode_time = None

    if not exploding_pieces:
        screen.blit(bomb, ((WIDTH - bomb.get_width()) // 2, (HEIGHT - bomb.get_height()) // 2))
        if pygame.time.get_ticks() % reset_time < 10:
            random_numbers = random.sample(range(64), 12)
            for idx in random_numbers:
                piece_image = get_sprite(idx)
                x = WIDTH // 2
                y = HEIGHT // 2
                exploding_pieces.append(ExplodingPiece(piece_image, x, y))
    else:
        exploding_pieces = [piece for piece in exploding_pieces if not piece.off_screen()]
        for piece in exploding_pieces:
            piece.update()
            piece.draw(screen)

        if not exploding_pieces:
            last_explode_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
