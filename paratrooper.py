"""Paratrooper."""
from parachute import Parachute
from pygame import image, mask, Rect, sprite, Vector2, time
from random import choice
from enum import Enum

GRAVITY = .1
CANOPY_DESCENT = 2
SURVIVABLE_DESCENT = 4.0
BAND_HEIGHT = 70  # Height of each flight band level
PARATROOPERS = "images/paratrooper.png"
WIDTH = 27
HEIGHT = 52
CROUCHED_SIZE = (27, 37)


class Status(Enum):
    """Paratrooper states."""

    FREE_FALL = 0
    CHUTE_DEPLOYED = 1
    CHUTE_SEVERED = 2
    LANDED = 3
    DEAD = 4


class Landing(Enum):
    """Paratrooper landing state."""

    NONE = 0
    ON_GROUND = 1
    ON_BUNKER = 2
    DEAD = 4


class Paratrooper(sprite.Sprite):
    """Paratrooper."""

    def __init__(self, drop_zone_x, over_bunker, flight_level,
                 max_flight_level, ground_y, bunker_y):
        """Initialize Paratrooper.

        Args:
            drop_zone_x(int):  Vertical drop zone X center coordinate
            over_bunker(bool): Indicates if paratrooper dropped over bunker
            flight_level(int): Numbered flight band 1 to n from top of screen
            max_flight_level(int): Maximum flight levels for the wave
            ground_y(int): Y coordinate of ground
            bunker_y(int): Y coordinate of bunker roof
        """
        super().__init__()
        self.sprite_sheet = image.load(PARATROOPERS).convert_alpha()
        self.ground_y = ground_y
        self.bunker_y = bunker_y
        if over_bunker:
            self.current_sprite_index = 4  # Demolition expert
        else:
            self.current_sprite_index = choice((0, 2))  # Airborne infantry
        self.over_bunker = over_bunker
        source_rect = Rect(self.current_sprite_index * WIDTH, 0, WIDTH, HEIGHT)
        self.image = self.sprite_sheet.subsurface(source_rect)
        self.mask = mask.from_surface(self.image)
        starting_location = Vector2(drop_zone_x,
                                    (flight_level + 1) * BAND_HEIGHT)
        self.rect = self.image.get_rect(midtop=starting_location)
        self.direction = Vector2(0, 1)
        self.state = Status.FREE_FALL
        self.deployment_y = (max_flight_level + 1) * BAND_HEIGHT + 103
        self.chute = Parachute(location=self.rect.midtop)
        # Used for sprite alternation
        self.last_update_time = time.get_ticks()
        self.index_adjust = 0

    def crouch(self):
        """Set sprite to crouch position."""
        source_rect = Rect(6 * WIDTH, 0, WIDTH, HEIGHT)
        self.image = self.sprite_sheet.subsurface(source_rect)
        self.mask = mask.from_surface(self.image)

    def draw(self, screen):
        """Draw Paratrooper.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        if self.state == Status.CHUTE_DEPLOYED:  # Draw parachute
            self.chute.draw(screen)
        screen.blit(self.image, self.rect)

    @property
    def on_ground(self):
        """Return if paratrooper is safely on ground."""
        return self.state == Status.LANDED

    @property
    def under_canopy(self):
        """Return if paratrooper is falling with chute deployed."""
        return self.state == Status.CHUTE_DEPLOYED

    def sever_parachute(self):
        """Sever parachute."""
        if self.state == Status.CHUTE_DEPLOYED:
            self.state = Status.CHUTE_SEVERED

    def update(self):
        """Update position of the Paratrooper.

        Returns:
            Landing(enum): Landing state
        """
        if self.state != Status.LANDED:
            if self.state == Status.FREE_FALL:
                self.direction.y += GRAVITY   # Simulate gravity
                if self.rect.y >= self.deployment_y:
                    self.state = Status.CHUTE_DEPLOYED
            elif self.state == Status.CHUTE_SEVERED:
                self.direction.y += GRAVITY   # Simulate gravity
                # Falling animiation
                now = time.get_ticks()
                if now - self.last_update_time > 100:  # 100 ms passed
                    self.last_update_time = now
                    self.index_adjust = (
                        0 if self.index_adjust == 1 else 1)
                    source_rect = Rect((self.current_sprite_index +
                                        self.index_adjust) * WIDTH, 0,
                                       WIDTH, HEIGHT)
                    self.image = self.sprite_sheet.subsurface(source_rect)
                    self.mask = mask.from_surface(self.image)
            elif self.state == Status.CHUTE_DEPLOYED:
                if self.direction.y > CANOPY_DESCENT:
                    self.direction.y -= 0.4
            self.rect.move_ip(self.direction)
            # Update parachute if deployed
            if self.state == Status.CHUTE_DEPLOYED:
                self.chute.update(self.rect.midtop)
            # Check for landing
            if self.over_bunker and self.rect.bottom >= self.bunker_y:
                if self.direction.y <= SURVIVABLE_DESCENT:
                    # Safe landing
                    self.rect.bottom = self.bunker_y
                    self.state = Status.LANDED
                    self.crouch()
                    return Landing.ON_BUNKER
                else:
                    self.state = Status.DEAD
                    return Landing.DEAD
            # Check for landing on ground
            if self.rect.bottom >= self.ground_y:
                if self.direction.y <= SURVIVABLE_DESCENT:
                    # Safe landing
                    self.rect.bottom = self.ground_y
                    self.state = Status.LANDED
                    source_rect = Rect(6 * WIDTH, 0, WIDTH, HEIGHT)
                    self.image = self.sprite_sheet.subsurface(source_rect)
                    self.mask = mask.from_surface(self.image)
                    return Landing.ON_GROUND
                else:
                    self.state = Status.DEAD
                    return Landing.DEAD
        return Landing.NONE

    def walk(self, dir):
        """Move paratrooper for demolishing bunker animation.

        Args:
            dir([int, int]): Direction and speed to walk
        """
        self.rect.move_ip(dir)
        now = time.get_ticks()
        if now - self.last_update_time > 100:  # 100 ms passed
            self.last_update_time = now
            self.index_adjust = (
                0 if self.index_adjust == 1 else 1)
            source_rect = Rect((self.current_sprite_index +
                               self.index_adjust) * WIDTH, 0,
                               WIDTH, HEIGHT)
            self.image = self.sprite_sheet.subsurface(source_rect)
