import pygame
from pygame.locals import *

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Paratrooper(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.spritesheet = pygame.image.load('paratrooper.png').convert_alpha()
        self.paratrooper_image = self.extract_paratrooper(0) # Extract the first sprite
        self.chute_image = pygame.image.load('parachute.png').convert_alpha()
        self.image = self.paratrooper_image
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.deployed = False

    def extract_paratrooper(self, index):
        # Given the size and layout of the spritesheet, extract the desired sprite
        width = 27
        height = 52
        x = index * width
        y = 0
        return self.spritesheet.subsurface(pygame.Rect(x, y, width, height))

    def draw(self, surface):
        if self.deployed:
            chute_rect = self.chute_image.get_rect(midbottom=self.rect.midtop)
            surface.blit(self.chute_image, chute_rect.topleft)
        surface.blit(self.image, self.rect.topleft)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Paratrooper Example')

paratrooper = Paratrooper(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

running = True
chute_timer = 3000 # 3 seconds in milliseconds
start_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    if current_time - start_time >= chute_timer and not paratrooper.deployed:
        paratrooper.deployed = True

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((255, 255, 255))  # Fill with white color
    paratrooper.draw(screen)  # Use custom draw method
    pygame.display.flip()
    pygame.time.wait(16)  # Approximately 60fps

pygame.quit()
