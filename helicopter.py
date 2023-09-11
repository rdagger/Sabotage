"""Helicopter."""
from math import copysign
from pygame import image, mask, Rect, sprite, Vector2, time

CHOPPER = "images/helicopter.png"
BAND_HEIGHT = 70  # Height of each flight band level


class Helicopter(sprite.Sprite):
    """Helicopter."""

    def __init__(self, screen_width, drops, direction_x, flight_level):
        """Initialize helicopter.

        Args:
            screen_width (int): Overall screen width of game
            drops([int]]):  List of X coodinate drop zones
            direction_x(int): Horizontal direction & speed of helicopter
            flight_level(int): Numbered flight bands 1 to n from top of screen
        """
        super().__init__()
        self.screen_width = screen_width
        self.flight_level = flight_level
        # Order drop zones
        self.drops = sorted(drops, reverse=copysign(1, direction_x) < 0)

        # Split the sprite sheet into individual images.
        sprite_sheet = image.load(CHOPPER)
        self.sprite_width = sprite_sheet.get_width() // 4
        self.sprite_height = sprite_sheet.get_height()
        self.sprites = [
            sprite_sheet.subsurface(Rect(i * self.sprite_width, 0,
                                         self.sprite_width,
                                         self.sprite_height))
            for i in range(4)
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
            self.image = self.sprites[2]  # Initial sprite facing right
        self.rect = self.image.get_rect()
        # Set initial position - aligned bottom center
        self.rect.midbottom = self.location
        self.mask = mask.from_surface(self.image)
        # Used for sprite alternation
        self.last_update_time = time.get_ticks()
        self.current_sprite_index = 0

    @property
    def course(self):
        """Return current direction and flight level."""
        return (1 if self.direction.x > 0 else -1, self.flight_level)

    def draw(self, screen):
        """Draw helicopter.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        screen.blit(self.image, self.rect)

    @property
    def out_of_bounds(self):
        """Determine if chopper has flown off screen."""
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
        """Update position of the helicopter.

        Returns:
            int: if paratrooper dropped indicating drop zone X coordinate
        """
        self.location += self.direction
        self.rect.midbottom = self.location

        # Update the sprite based on direction
        now = time.get_ticks()
        if now - self.last_update_time > 100:  # 100 ms passed
            self.last_update_time = now
            # Animate helicopter blades
            if self.direction.x > 0:
                self.current_sprite_index = (
                    0 if self.current_sprite_index == 1 else 1)
            elif self.direction.x < 0:
                self.current_sprite_index = (
                    2 if self.current_sprite_index == 3 else 3)
            self.image = self.sprites[self.current_sprite_index]
            self.mask = mask.from_surface(self.image)

        # Check for drop zone
        if len(self.drops):
            if ((self.direction.x > 0 and self.location.x >= self.drops[0]) or
               (self.direction.x < 0 and self.location.x <= self.drops[0])):
                return self.drops.pop(0)
        return None
