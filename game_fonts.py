"""Game fonts."""
from enum import Enum
from os import path
from pygame import font, transform

FONT_FOLDER = "fonts"


class Size(Enum):
    """Font sizes."""

    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    HUGE = 4
    LEVEL = 5
    CODA = 6


class GameFonts:
    """Create class for tail sprites that look like squares."""

    def __init__(self):
        """Game fonts constructor."""
        self.small = font.Font(path.join(FONT_FOLDER, "E4_2017.ttf"), 20)
        self.medium = font.Font(path.join(FONT_FOLDER, "PressStart2P.ttf"), 20)
        self.large = font.Font(path.join(FONT_FOLDER, "PressStart2P.ttf"), 30)
        self.huge = font.Font(path.join(FONT_FOLDER, "graphicpixel.ttf"), 130)
        self.level = font.Font(path.join(FONT_FOLDER, "ka1.ttf"), 72)
        self.coda = font.Font(path.join(FONT_FOLDER, "puente.ttf"), 96)

    def draw(self, text, size, position, screen, color,
             background=None, center=False, flip=False):
        """Draw text.

        Args:
            text(string): Text to draw.
            size(Enum): Font & size (SMALL, MEDIUM, LARGE, HUGE, CODA).
            position((int, int)): X, Y position to draw font.
            screen(pygame.Surface): Graphical window to display graphics.
            color((int, int, int)): RGB text color.
            background((int, int, int)): RGB background color. (default=None)
            center(bool): Center text on specified position.  (default=False)
            flip(bool): Flip text 180 degrees. (default=False)
        """
        if size == Size.SMALL:
            text = self.small.render(text, True, color, background)
        elif size == Size.MEDIUM:
            text = self.medium.render(text, True, color, background)
        elif size == Size.LARGE:
            text = self.large.render(text, True, color, background)
        elif size == Size.HUGE:
            text = self.huge.render(text, True, color, background)
        elif size == Size.LEVEL:
            text = self.level.render(text, True, color, background)
        elif size == Size.CODA:
            text = self.coda.render(text, True, color, background)
        else:
            raise ValueError("Invalid size.")

        text_rect = text.get_rect(center=position)
        if center:
            position = (position[0] - text_rect.width // 2,
                        position[1] - text_rect.height // 2)

        if flip:
            flipped_surface = transform.rotate(text, 180)
            screen.blit(flipped_surface, position)
        else:
            screen.blit(text, position)

    def measure(self, text, size):
        """Measure width and height of text.

        Args:
            text(string): Text to measure.
            size(Enum): Determines font and size (SMALL, MEDIUM, LARGE, HUGE).
        """
        if size == Size.SMALL:
            return self.small.size(text)
        elif size == Size.MEDIUM:
            return self.medium.size(text)
        elif size == Size.LARGE:
            return self.large.size(text)
        elif size == Size.HUGE:
            return self.huge.size(text)
        elif size == Size.LEVEL:
            return self.level.size(text)
        elif size == Size.CODA:
            return self.coda.size(text)
        else:
            raise ValueError("Invalid size.")
