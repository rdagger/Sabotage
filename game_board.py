"""Sabotage game board."""
from game_fonts import GameFonts, Size
from game_sounds import GameSounds
from pygame import (
    Color, draw, event, image, key, Rect, sprite, quit, time, transform)
from pygame.locals import KEYDOWN, KEYUP, QUIT


BUNKER = "images/bunker.png"
LIVES = "images/lives.png"


class Board:
    """Sabotage game board."""

    def __init__(self, screen_width, screen_height, key_select, key_exit):
        """Create game board.

        Args:
            screen_width (int): Overall screen width of game.
            screen_height (int): Overall screen height of game.
            key_select(pygame.key): Keyboard key for selection
            key_exit(pygame.key): Keyboard key to exit game
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center = (screen_width // 2, screen_height // 2)

        self.key_select = key_select
        self.key_exit = key_exit

        self.fonts = GameFonts()

        h = self.fonts.medium.get_height()
        self.ground_y = screen_height - h - 6
        self.ground_rect = Rect(0, self.ground_y, screen_width, h + 6)

        self.bunker = image.load(BUNKER)
        self.bunker_pos = (((screen_width - self.bunker.get_width()) // 2),
                           self.ground_y - self.bunker.get_height())
        self.bunker_rect = self.bunker.get_rect(topleft=self.bunker_pos)

        self.lives = image.load(LIVES)
        self.lives_rect = self.bunker.get_rect()
        self.score_width, score_height = self.fonts.measure("000000",
                                                            Size.MEDIUM)
        self.score_y = self.screen_height - (score_height + 1)
        self.lives_width = self.lives.get_width()
        self.lives_y = self.screen_height - (self.lives.get_height() + 1)
        self.sounds = GameSounds()

        self.border = sprite.Group()

    def draw(self, screen):
        """Draw the play area.

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
        """
        # Draw ground
        draw.rect(screen, "forestgreen", self.ground_rect)

        # Draw bunker
        screen.blit(self.bunker, self.bunker_pos)

    def draw_fps(self, screen, clock):
        """Draw frame frate (FPS).

        Args:
            screen(pygame.Surface): Graphical window to display graphics.
            clock(pygame.time.Clock): Game clock
        """
        fps_text = f"FPS: {int(clock.get_fps())}"
        fps_width, fps_height = self.fonts.measure("FPS: 00", Size.SMALL)
        fps_pos = ((self.screen_width - fps_width) // 2,
                   self.screen_height - fps_height)
        self.fonts.draw(fps_text, Size.SMALL, fps_pos, screen,
                        Color("Yellow"), center=False)

    def draw_score(self, scores, lives, screen, current_player):
        """Display the player's score.

        Args:
            scores((int,int)): The scores for players 1 and 2
            lives((int,int)): The lives left for players 1 and 2
            screen(pygame.Surface): Graphical window to display graphics
            current_player(int): Player ID of current player
        """
        for player_id in range(len(scores)):
            color = "white" if player_id == current_player else "grey"
            score_text = f"{scores[player_id]:0>6}"
            score_x = ((self.screen_width // 4 +
                        self.screen_width // 2 * player_id) -
                       self.score_width // 2)
            self.fonts.draw(score_text, Size.MEDIUM, (score_x, self.score_y),
                            screen, Color(color))
            for life in range(lives[player_id] + 1):
                if player_id:
                    lives_x = (score_x + self.score_width +
                               (self.lives_width + 5) * (life + 1))
                else:
                    lives_x = score_x - (self.lives_width + 5) * (life + 2)
                screen.blit(self.lives, (lives_x, self.lives_y))

    def display_wave_number(self, wave_number, player_id, cocktail,
                            screen, display, delay=2500):
        """Display wave number.

        Args:
            wave_number(int): Wave number.
            player_id(int): ID of current player (zero based)
            cocktail(bool): Indicates if cocktail mode enabled
            screen(pygame.Surface): Graphical window to display graphics
            display(pygame.display): Visual output
            delay(int): Delay to show wave number on screen (milliseconds)
        """
        h = self.fonts.level.get_height()
        center_x, center_y = self.center
        level_text = f"Wave {wave_number}"
        self.fonts.draw(level_text,
                        Size.LEVEL,
                        (center_x, center_y - h),
                        screen,
                        Color("white"),
                        center=True)
        ready_text = f"Player {player_id + 1} Get Ready!"
        self.fonts.draw(ready_text,
                        Size.LARGE,
                        (center_x, center_y + h),
                        screen,
                        Color("turquoise"),
                        center=True)

        # Check for cocktail mode
        if cocktail and player_id == 1:
            # Rotate text 180 degrees
            text_rect = Rect(0, center_y - 1.5 * h, self.screen_width, 3 * h)
            text_subsurface = screen.subsurface(text_rect)
            rotated_text_subsurface = transform.rotate(text_subsurface, 180)
            screen.blit(rotated_text_subsurface, text_rect.topleft)

        display.flip()
        waiting = True
        pause = time.get_ticks()
        while waiting:  # Pause until CTRL pressed or ESC to quit
            if time.get_ticks() - pause > delay:
                break

    def game_over(self, level, screen, display):
        """Display game over and wait for select key press and release.

        Args:
            level(int): Level number to resume
            screen(pygame.Surface): Graphical window to display graphics.
            display(pygame.display): Visual output.
        """
        game_text = " Game "
        _, game_height = self.fonts.measure(game_text, Size.CODA)
        game_y = self.center[1] - game_height * .8
        self.fonts.draw(game_text,
                        Size.CODA,
                        (self.center[0], game_y),
                        screen,
                        Color("white"),
                        center=True)

        over_text = " Over "
        self.fonts.draw(over_text,
                        Size.CODA,
                        self.center,
                        screen,
                        Color("white"),
                        center=True)

        msg_text = f"Press {key.name(self.key_select).upper()} to resume"
        msg_text += f" LeveL {level}"
        msg_text += f" or {key.name(self.key_exit).upper()} to exit."
        msg_y = self.center[1] + self.center[1] // 2
        self.fonts.draw(msg_text,
                        Size.SMALL,
                        (self.center[0], msg_y),
                        screen,
                        Color("yellow"),
                        center=True)

        display.flip()
        waiting = True
        event.clear()
        while waiting:  # Pause until CTRL pressed or ESC to quit
            for e in event.get():
                if (e.type == QUIT or
                        e.type == KEYDOWN and e.key == self.key_exit):
                    quit()
                    exit()
                elif e.type == KEYUP and e.key == self.key_select:
                    waiting = False
