import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 1024

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Helicopter Explosion")

# Load the images
helicopter = pygame.image.load("helicopter.png")
sprite_sheet = pygame.image.load("explosion_helicopter.png")
heli_width = 118
heli_height = 57

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
    x = idx * 25
    return sprite_sheet.subsurface(pygame.Rect(x, 0, 25, 25))

clock = pygame.time.Clock()
exploding_pieces = []
reset_time = 4000
last_explode_time = None

running = True
rotor = True
counter = 0
while running:
    counter += 1
    screen.fill("deepskyblue")

    if last_explode_time and pygame.time.get_ticks() - last_explode_time >= reset_time:
        exploding_pieces = []
        last_explode_time = None

    if not exploding_pieces:
        if not counter % 5:
            rotor = not rotor  # Alternate helicopter rotor sprite to rotate blades
            counter = 0
        if rotor:
            area = pygame.Rect(0, 0, heli_width, heli_height)
        else:
            area = pygame.Rect(heli_width, 0, heli_width, heli_height)
        screen.blit(helicopter,
                    ((WIDTH - heli_width) // 2, (HEIGHT - heli_height) // 2),
                    area)
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
