"""Explosion."""
from pygame import image, mask, Rect, sprite, transform, Vector2
from random import sample, uniform

GRAVITY = .2
SPRITESHEETS = {
    "bomb": "images/explosion_bomb.png",
    "helicopter": "images/explosion_helicopter.png",
    "jet": "images/explosion_jet.png",
    "paratrooper": "images/explosion_paratrooper.png",
    "turret": "images/explosion_turret.png"
}

SIZES = {
    "bomb": (12, 12),
    "helicopter": (25, 25),
    "jet": (25, 25),
    "paratrooper": (25, 15),
    "turret": (25, 25)
}


class Shrapnel(sprite.Sprite):
    """Shrapnel."""

    def __init__(self, image, starting_location, initial_velocity, hazardous):
        """Initialize Shrapnel.

        Args:
            image(pygame.image): Sprite image
            starting_location((int, int)): starting location
            initial_velocity((int, int)): Initial velocity of exploded object
            hazardous(bool): Shrapnel is hazardous to other objects
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=starting_location)
        self.direction = Vector2(initial_velocity)
        self.direction.x += uniform(-3, 3)
        self.direction.y += uniform(-5, 3)
        self.angular_velocity = uniform(-5, 5)
        self.angle = 0
        self.hazardous = hazardous
        if self.hazardous:
            self.mask = mask.from_surface(self.image)

    def draw(self, surface):
        """Draw shrapnel."""
        rotated_image = transform.rotate(self.image, self.angle)
        surface.blit(rotated_image, self.rect.center)

    def update(self):
        """Update position of the shrapnel."""
        self.angle += self.angular_velocity
        self.direction.y += GRAVITY  # Increase Y speed to simulate gravity
        self.rect.move_ip(self.direction)


class Explosion:
    """Explosion."""

    def __init__(self, screen_width, screen_height, blast_center, blast_type,
                 initial_velocity, hazardous=True):
        """Initialize explosion.

        Args:
            screen_width (int): Overall screen width of game
            screen_height (int): Overall screen height of game
            blast_center((int, int)): Blast center
            blast_type(string): Type of object exploding
            initial_velocity((int, int)): Initial velocity of exploded object
            hazardous(bool): Generates shrapnel hazardous to other objects
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        sprite_sheet = image.load(SPRITESHEETS[blast_type])
        self.exploding_pieces = sprite.Group()
        if blast_type == "turret":
            random_numbers = sample(range(0, 12), 6) + sample(range(5, 64), 32)
            hazard_range = 11
        else:
            random_numbers = sample(range(0, 5), 1) + sample(range(5, 64), 11)
            hazard_range = 4
        for index in random_numbers:
            source = Rect(index * SIZES[blast_type][0], 0,
                          SIZES[blast_type][0], SIZES[blast_type][1])
            self.exploding_pieces.add(
                Shrapnel(sprite_sheet.subsurface(source),
                         blast_center,
                         initial_velocity,
                         hazardous and index <= hazard_range,  # Hazardous
                         ))

    @property
    def count(self):
        """Return the current number of exploding pieces."""
        return len(self.exploding_pieces)

    def draw(self, screen):
        """Draw all exploding pieces.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        for piece in self.exploding_pieces:
            piece.draw(screen)

    def get_hazardous(self):
        """Return hazardous sprites.

        Returns:
            [pygame.sprites]:  All hazardous sprites
        """
        return [s for s in self.exploding_pieces if s.hazardous]

    def update(self):
        """Update exploding pieces."""
        for piece in self.exploding_pieces:
            piece.update()
            if (piece.rect.right < 0 or
                    piece.rect.left > self.screen_width - 1 or
                    piece.rect.top > self.screen_height - 1):
                self.exploding_pieces.remove(piece)
