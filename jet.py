"""Jet."""
from pygame import image, mask, Rect, sprite, Vector2
from random import random, randint

JET = "images/jet.png"
BAND_HEIGHT = 70  # Height of each flight band level

HORIZ_RANGE = {  # Bomb trajectory speed to X distance
    2: 40,
    3: 80,
    4: 125,
    5: 175,
    6: 225,
    7: 275,
}


class Jet(sprite.Sprite):
    """Jet."""

    def __init__(self, screen_width, direction_x, flight_level, bunker_rect):
        """Initialize jet.

        Args:
            screen_width (int): Overall screen width of game
            direction_x(int): Horizontal direction & speed of jet
            flight_level(int): Numbered flight bands 1 to n from top of screen
            bunker_rect(Rect): Rectangle outline of bunker
        """
        super().__init__()
        self.screen_width = screen_width
        self.flight_level = flight_level

        # Split the sprite sheet into individual images.
        sprite_sheet = image.load(JET).convert_alpha()
        self.sprite_width = sprite_sheet.get_width() // 2
        self.sprite_height = sprite_sheet.get_height()
        self.sprites = [
            sprite_sheet.subsurface(Rect(i * self.sprite_width, 0,
                                         self.sprite_width,
                                         self.sprite_height))
            for i in range(2)
        ]

        self.direction = Vector2(direction_x, 0)
        if direction_x > 0:  # Left to right
            self.location = Vector2(
                5 - self.sprite_width // 2,
                (flight_level + 1) * BAND_HEIGHT)
            self.image = self.sprites[0]  # Initial sprite facing left
        else:  # Right to left
            self.location = Vector2(
                (self.screen_width - 5) + self.sprite_width // 2,
                (flight_level + 1) * BAND_HEIGHT)
            self.image = self.sprites[1]  # Initial sprite facing right

        if random() < .25:  # 25% of jets don't drop bombs
            self.bombs = 0
        else:
            self.bombs = 1
        # Calculate when to drop bomb
        target_x = randint(bunker_rect.left + 10, bunker_rect.right - 10)
        if self.direction.x > 0:
            self.drop_x = target_x - HORIZ_RANGE[abs(self.direction.x)]
        else:
            self.drop_x = target_x + HORIZ_RANGE[abs(self.direction.x)]

        self.rect = self.image.get_rect()
        # Set initial position - aligned bottom center
        self.rect.midbottom = self.location
        self.mask = mask.from_surface(self.image)

    @property
    def course(self):
        """Return current direction and flight level."""
        return (1 if self.direction.x > 0 else -1, self.flight_level)

    def draw(self, screen):
        """Draw jet.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        screen.blit(self.image, self.rect)

    @property
    def out_of_bounds(self):
        """Determine if jet has flown off screen."""
        x = self.location.x
        if x > 0:
            # Left to right
            if x - self.sprite_width // 2 > self.screen_width:
                return True
        else:
            # Right to left
            if x + self.sprite_width // 2 < 0:
                return True
        return False

    def update(self):
        """Update jet position.

        Returns:
            bool: True if bomb is dropped
        """
        self.location += self.direction
        self.rect.midbottom = self.location

        if self.bombs > 0:  # Check if bomb should be dropped
            if ((self.direction.x > 0 and
                 self.location.x > self.drop_x) or
                (self.direction.x < 0 and
                 self.location.x < self.drop_x)):
                self.bombs = 0
                return True
        return False
