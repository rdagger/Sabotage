"""Bullet."""
from pygame import image, mask, Rect, sprite

BULLETS = "images/bullets.png"
BULLET_ANGLES = {
    -90: 0,
    -65: 9,
    -45: 8,
    -20: 7,
    -10: 6,
    0: 5,
    10: 4,
    20: 3,
    45: 2,
    65: 1,
    90: 0,
}
WIDTH = 10
HEIGHT = 10


class Bullet(sprite.Sprite):
    """Bullet."""

    def __init__(self, starting_location, muzzle_vector):
        """Initialize bullet.

        Args:
            starting_location(Vector2) Starting X,Y coordinates of bullet
            muzzle_vector(Vector2):  X, Y direction & speed of bullet
        """
        super().__init__()
        sprite_sheet = image.load(BULLETS).convert_alpha()
        angle = round(muzzle_vector.as_polar()[1]) + 90  # Angle of bullet
        source_rect = Rect(BULLET_ANGLES[angle] * WIDTH, 0, WIDTH, HEIGHT)
        self.image = sprite_sheet.subsurface(source_rect)
        self.mask = mask.from_surface(self.image)
        self.location = starting_location
        self.rect = self.image.get_rect(center=starting_location)
        self.direction = muzzle_vector

    def draw(self, screen):
        """Draw bullet.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        screen.blit(self.image, self.rect)

    def update(self):
        """Update position of the bullet."""
        self.location += self.direction
        self.rect.center = self.location
