"""Parachute."""
from pygame import image, mask, sprite

PARACHUTE = "images/parachute.png"


class Parachute(sprite.Sprite):
    """Parachute."""

    def __init__(self, location):
        """Initialize Parachute.

        Args:
            location(Vector2) Starting X,Y midbottom of parachute
        """
        super().__init__()
        self.image = image.load(PARACHUTE).convert_alpha()
        self.mask = mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom=location)

    def draw(self, screen):
        """Draw parachute.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        screen.blit(self.image, self.rect)

    def update(self, location):
        """Update position of the parachute.

        Args:
            location((int, int)): X, Y coordinates to draw parachute
        """
        self.rect.midbottom = location
