"""Bomb."""
from math import copysign
from pygame import image, sprite, transform, Vector2

BOMB = "images/bomb.png"
GRAVITY = 0.08

WIDTH = 22
HEIGHT = 30


class Bomb(sprite.Sprite):
    """Bomb."""

    def __init__(self, starting_location, jet_vector):
        """Initialize bomb.

        Args:
            starting_location(Vector2) Starting X,Y coordinates of bomb
            jet_vector(Vector2):  X, Y direction & speed of jet
        """
        super().__init__()
        self.image = image.load(BOMB)
        self.rect = self.image.get_rect(center=starting_location)
        self.direction = Vector2(jet_vector)
        self.angle = 90 * copysign(1, self.direction.x)

    def draw(self, screen):
        """Draw bomb.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        rotated_bomb = transform.rotate(self.image, self.angle)
        rotated_rect = rotated_bomb.get_rect(center=self.rect.center)
        screen.blit(rotated_bomb, rotated_rect)

    def update(self):
        """Update position of the bomb."""
        # Adjust bomb angle downwards during fall
        if ((self.direction.x > 0 and self.angle > 0) or
                (self.direction.x < 0 and self.angle < 0)):
            self.angle += (-copysign(1, self.direction.x))

        self.direction.x *= 0.981  # Reduce X speed to simulate drag
        self.direction.y += GRAVITY  # Increase Y speed to simulate gravity
        self.rect.move_ip(self.direction.x, self.direction.y)
