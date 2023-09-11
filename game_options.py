"""Sabotage game options."""
from game_fonts import GameFonts, Size
from pygame import Color, draw, display, event, image, key, quit, Rect, Surface
from pygame.locals import KEYDOWN, KEYUP, MOUSEMOTION, QUIT

TITLE = "images/title.png"
MAX_PLAYERS = 2


class Options:
    """Sabotage game options."""

    def __init__(self, key_select, key_decrement, key_increment, key_exit):
        """Game options constructor.

        Args:
            key_select(pygame.key): Keyboard key for selection
            key_decrement(pygame.key): Keyboard key to increment value
            key_increment(pygame.key): Keyboard key to decrement value
            key_exit(pygame.key): Keyboard key to exit game
        """
        self.players = 1  # Number of players
        self.key_select = key_select
        self.key_decrement = key_decrement
        self.key_increment = key_increment
        self.key_exit = key_exit
        self.title = image.load(TITLE)

    def prompt(self, screen):
        """Prompt for the number of players.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        fonts = GameFonts()
        input_text = "ENTER # OF PLAYERS"
        screen_width, screen_height = screen.get_size()
        play_area = Rect(int(screen_width * 0.15),
                         int(screen_height * 0.1),
                         int(screen_width * 0.70),
                         int(screen_height * 0.8))

        title_pos = (((screen_width - self.title.get_width()) // 2),
                     int(screen_height * 0.15))
        input_text_pos = (
            self.title.get_rect().bottom
            + ((play_area.bottom - self.title.get_rect().bottom) // 2)
            + fonts.large.get_height() // 2)
        input_value_pos = (
            self.title.get_rect().bottom
            + ((play_area.bottom - self.title.get_rect().bottom) // 2)
            + fonts.huge.get_height())
        dir_text = "LEFT/RIGHT Keys or Mouse to SeLeCT - "
        dir_text += f"{key.name(self.key_select).upper()} to Continue - "
        dir_text += f"{key.name(self.key_exit).upper()} to Exit"
        dir_pos = (play_area.centerx, play_area.bottom -
                   fonts.small.get_height())

        # Create a new surface for the gradient
        gradient_surface = Surface((screen_width, screen_height))
        # Define the gradient colors
        colors = [Color("olivedrab"),
                  Color("olivedrab1"),
                  Color("olivedrab2"),
                  Color("olivedrab3"),
                  Color("olivedrab4"),
                  Color("olive")]
        # Define the transition height
        trans_height = screen_height // (len(colors) - 1)
        for i in range(len(colors) - 1):
            for y in range(trans_height):
                # Get the start and end colors
                start_color = colors[i]
                end_color = colors[i + 1]
                # Calculate the transition ratio
                ratio = y / trans_height
                # Interpolate the color
                color = [int(start * (1 - ratio) + end * ratio) for start,
                         end in zip(start_color, end_color)]
                # Draw the line on the gradient surface
                draw.line(gradient_surface, color, (0, i * trans_height + y),
                          (screen_width, i * trans_height + y))
        x_movement = 0
        while True:
            for e in event.get():
                if (e.type == QUIT or
                        e.type == KEYDOWN and e.key == self.key_exit):
                    quit()
                    exit()
                elif e.type == KEYDOWN:
                    if e.key == self.key_decrement and self.players > 1:
                        self.players -= 1
                    elif (e.key == self.key_increment and
                          self.players < MAX_PLAYERS):
                        self.players += 1

                elif e.type == MOUSEMOTION:
                    # Check mouse X movement
                    x_movement += e.rel[0]
                    if x_movement > 25:
                        self.players = 2
                    elif x_movement < -25:
                        self.players = 1
                elif e.type == KEYUP:
                    if e.key == self.key_select:
                        return

            # Blit the gradient surface onto the screen
            screen.blit(gradient_surface, (0, 0))

            draw.rect(screen, Color('darkgreen'), play_area, 0)  # Play area

            # Sabotage title image
            screen.blit(self.title, title_pos)
            # Directions
            fonts.draw(dir_text, Size.SMALL, dir_pos,
                       screen, Color(76, 235, 0), center=True)
            # Set input either players or games
            input_value = self.players
            # Draw input prompt and value
            fonts.draw(input_text, Size.LARGE,
                       (play_area.centerx, input_text_pos),
                       screen, Color(226, 63, 0), center=True)
            fonts.draw(str(input_value), Size.HUGE,
                       (play_area.centerx, input_value_pos),
                       screen, Color("white"), center=True)
            display.flip()
