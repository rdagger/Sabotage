"""Turret."""
from pygame import image, Rect, Vector2

ANIMATION_DELAY = 4
BULLET_SPEED = 10
PATH = "images/gun"
POSITIONS = [-90, -65, -45, -20, -10, 0, 10, 20, 45, 65, 90]
TURRET_OFFSETS = {
    -90: -25,
    -65: -20,
    -45: -15,
    -20: -5,
    -10: -3,
    0: 0,
    10: 3,
    20: 5,
    45: 15,
    65: 20,
    90: 25
}

MUZZLE_OFFSETS = {
    -90: (-38, -23),
    -65: (-32, -38),
    -45: (-23, -46),
    -20: (-12, -53),
    -10: (-10, -55),
    0: (0, -55),
    10: (10, -55),
    20: (12, -53),
    45: (23, -46),
    65: (32, -38),
    90: (38, -23)
}


class Turret:
    """Turret."""

    def __init__(self, bunker_midtop, screen_width):
        """Initialize turret.

        Args:
            midtop((int, int)): Middle top position of bunker
            screen_width (int): Overall screen width of game.
        """
        self.bunker_midtop = Vector2(bunker_midtop)
        self.x, self.y = bunker_midtop
        self.y += 2
        self.screen_width = screen_width

        # Start at angle 0
        self.current_angle_index = POSITIONS.index(0)

        # Load the sprites for each angle
        self.sprites = {}
        for angle in POSITIONS:
            self.sprites[angle] = [
                image.load(f"{PATH}{angle if angle != 0 else f'0{angle}'}.png")
                for _ in range(5)
            ]
        # Starting sprite is gun unfired at angle 0
        self.current_sprite = self.sprites[0][0]
        self.animation_index = 0  # Index to track firing animation
        self.animation_count = 0
        # Initial mouse position
        self.mouse = screen_width // 2
        self.mouse_segment = screen_width / len(POSITIONS)

    @property
    def center(self):
        """Return center of turret."""
        return (self.x, self.y - self.current_sprite.get_height() // 2)

    def clear_animation(self):
        """Clear any active animations."""
        self.animation_index = 0
        self.animation_count = 0
        self.update_sprite()

    def draw(self, screen):
        """Draw turret.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        sprite_width = self.current_sprite.get_width() // 5
        sprite_height = self.current_sprite.get_height()
        # Calculate the rectangle for the first sprite
        x = self.animation_index * sprite_width
        source_rect = Rect(x, 0, sprite_width, sprite_height)
        target_rect = Rect(0, 0, sprite_width, sprite_height)

        # Set the midbottom position
        target_rect.midbottom = (self.x, self.y)
        screen.blit(self.current_sprite, target_rect, source_rect)

        # Check if firing
        if self.animation_index > 0:
            self.animation_count += 1
            if self.animation_count >= ANIMATION_DELAY:
                self.animation_count = 0
                self.animation_index += 1
                if self.animation_index > 4:
                    self.animation_index = 0
                self.update_sprite()
        """
        # Draw project bullet trajectory
        draw.circle(screen, (255, 0, 0), self.get_muzzle_pos(), 5)
        trajectory_end = (self.get_muzzle_pos() +
                          self.get_muzzle_vector().normalize() * 900)
        draw.line(screen, (255, 255, 0), self.get_muzzle_pos(),
                  trajectory_end, 1)
        """

    def get_muzzle_pos(self):
        """Get muzzle position."""
        return (self.bunker_midtop +
                MUZZLE_OFFSETS[POSITIONS[self.current_angle_index]])

    def get_muzzle_vector(self):
        """Get muzzle vector (direction and speed)."""
        angle = POSITIONS[self.current_angle_index] - 90
        return Vector2(BULLET_SPEED, 0).rotate(angle)

    def move(self, mouse, relative):
        """Move turret counter-clockwise or clockwise.

        Args:
            mouse(int): Mouse actual position or relative
            relative(bool): True=relative, False-actual
        """
        # Don't move while firing
        if self.animation_index != 0:
            return
        if relative:
            self.mouse += mouse
        else:
            self.mouse = mouse
        segment_index = min(int(self.mouse / self.mouse_segment),
                            len(POSITIONS) - 1)

        self.current_angle_index = segment_index

        # Adjust gun offset
        self.x = self.bunker_midtop[0] + TURRET_OFFSETS[
            POSITIONS[self.current_angle_index]]
        self.update_sprite()

    def move_keyboard(self, direction):
        """Move turret counter-clockwise or clockwise.

        Args:
            mouse(int): Mouse actual position or relative
            direction(string): Left=counter-clockwise, Right=clockwise
        """
        if direction == "left" and self.current_angle_index > 0:
            self.current_angle_index -= 1
        elif direction == "right" and (self.current_angle_index <
                                       len(POSITIONS) - 1):
            self.current_angle_index += 1
        else:
            return

        # Adjust gun offset
        self.x = self.bunker_midtop[0] + TURRET_OFFSETS[
            POSITIONS[self.current_angle_index]]
        self.update_sprite()

    def fire(self):
        """Animate the firing."""
        self.animation_index = 1
        self.animation_count = 0
        self.update_sprite()

    def update_sprite(self):
        """Update sprite."""
        self.current_sprite = self.sprites[
            POSITIONS[self.current_angle_index]
            ][self.animation_index]
