import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 1024

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turret Explosion")

# Load the images
bunker = pygame.image.load("bunker.png")
bunker_rect = bunker.get_rect()
bunker_rect.midtop = ((WIDTH - bunker_rect.width) // 2, HEIGHT - bunker_rect.height)
sprite_sheet = pygame.image.load("explosion_turret.png")
turret = pygame.image.load("turret.png")
turret_rect = turret.get_rect()
turret_rect.midbottom = bunker_rect.midtop

# Colors
BLACK = (0, 0, 0)


class ExplodingPiece:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.y_velocity = random.uniform(-14, 3)
        self.x_velocity = random.uniform(-7, 7)
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
    return sprite_sheet.subsurface(pygame.Rect(x, 0, 25, 15))

clock = pygame.time.Clock()
exploding_pieces = []
reset_time = 3000
last_explode_time = None

running = True
while running:
    screen.fill("deepskyblue")

    screen.blit(bunker, bunker_rect)

    if last_explode_time and pygame.time.get_ticks() - last_explode_time >= reset_time:
        exploding_pieces = []
        last_explode_time = None

    if not exploding_pieces:
        screen.blit(turret, turret_rect)
        if pygame.time.get_ticks() % reset_time < 10:
            random_numbers = random.sample(range(64), 32)
            for idx in random_numbers:
                piece_image = get_sprite(idx)
                x = turret_rect.centerx
                y = turret_rect.centery
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
