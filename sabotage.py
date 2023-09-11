"""Pygame Sabotage."""
from bomb import Bomb
from bullet import Bullet
from configparser import ConfigParser
from enum import Enum
from explosion import Explosion
from game_board import Board
from game_options import Options
from game_sounds import GameSounds, END_SOUND_EVENT
import gc
from helicopter import Helicopter
from jet import Jet
from paratrooper import CROUCHED_SIZE, Paratrooper, Landing, Status
from pygame import display, event, init, mouse, quit, sprite, time, transform
from pygame.locals import FULLSCREEN, KEYDOWN, MOUSEMOTION, QUIT
from random import randint
from sys import exit, modules
from turret import Turret
from waves import Waves
from zones import Zones

PARATROOPER_SCORE = 25
HELICOPTER_SCORE = 50
JET_SCORE = 75
BOMB_SCORE = 250
BULLET_PENALTY = 10


class Demolition(Enum):
    """Demolition stages."""

    NONE = 0
    PENDING = 1
    ACTIVE = 2


class Game:
    """Sabotage."""

    def __init__(self):
        """Game constructor."""
        init()  # Initialize pygame library
        self.clock = time.Clock()
        # Load game settings file
        config = ConfigParser()
        config.read('settings.ini')
        self.screen_width = config.getint('GameSettings', 'screen_width')
        self.screen_height = config.getint('GameSettings', 'screen_height')
        full_screen = config.getboolean('GameSettings', 'full_screen')
        self.fps = config.getint('GameSettings', 'speed')
        self.total_lives = config.getint('GameSettings', 'lives')
        self.mouse_rel = config.getboolean('GameSettings', 'mouse_relative')
        self.show_fps = config.getboolean('GameSettings', 'frame_rate')
        self.cocktail = config.getboolean('GameSettings', 'cocktail_mode')

        # Get keyboard input keys for each player
        self.input_keys = {}
        for player_num in range(1, 3):
            player = "Player{}".format(player_num)
            self.input_keys[player] = {}
            key = config.get(player, "button1_key")
            self.input_keys[player]["button1"] = getattr(
                modules["pygame"], key)
            for direction in ["left", "right"]:
                key = config.get(player, f"{direction}_key")
                self.input_keys[player][direction] = getattr(
                    modules["pygame"], key)

        self.key_select = getattr(modules["pygame"],
                                  config.get("Player1", "select_key"))
        self.key_exit = getattr(modules["pygame"],
                                config.get("Player1", "exit_key"))
        # Initialize screen
        if full_screen:
            self.screen = display.set_mode((0, 0), FULLSCREEN)
        else:
            self.screen = display.set_mode((self.screen_width,
                                            self.screen_height))

        self.board = Board(self.screen_width, self.screen_height,
                           self.key_select,
                           self.key_exit)
        self.options = Options(self.key_select,  # In game user options
                               self.input_keys["Player1"]["left"],
                               self.input_keys["Player1"]["right"],
                               self.key_exit)
        self.options.prompt(self.screen)  # Prompt user for options
        self.sounds = GameSounds()
        self.turret = Turret(self.board.bunker_rect.midtop, self.screen_width)
        self.bunker_destroyed = False
        self.demolition_stage = Demolition.NONE
        self.bullets = []
        self.explosions = []
        self.zones = Zones(self.screen_width, self.board.bunker_rect.width,
                           self.options.players)
        self.helicopters = sprite.Group()
        self.jets = sprite.Group()
        self.bombs = []
        self.reset()
        self.render()
        self.board.display_wave_number(1, 0, self.cocktail,
                                       self.screen, display)

    def collision_detection(self):
        """Detect collisions between game objects."""
        for bullet in self.bullets:
            if self.check_collision(bullet):
                self.bullets.remove(bullet)

        for explosion in self.explosions:
            shrapnel = explosion.get_hazardous()
            for fragment in shrapnel:
                if self.check_collision(fragment):
                    explosion.exploding_pieces.remove(fragment)

    def check_collision(self, projectile):
        """Detect collision between projectile and game objects.

        Args:
            projectile(pygame.sprite):  Either a bullet or hazardous debris
        """
        paratroopers = self.paratroopers[self.current_player]
        targets = [
            (paratroopers, PARATROOPER_SCORE, 'paratrooper'),
            (self.jets, JET_SCORE, 'jet'),
            (self.helicopters, HELICOPTER_SCORE, 'helicopter'),
            (self.bombs, BOMB_SCORE, 'bomb')
        ]

        for target_list, score, target_type in targets:
            for target in target_list:
                if sprite.collide_mask(projectile, target):
                    # Sounds
                    if target_type in ['jet', 'helicopter', 'bomb']:
                        self.sounds.play("explode")
                    elif target_type == "paratrooper":
                        self.sounds.play("shot")
                    # Add explosion
                    self.explosions.append(Explosion(
                        self.screen_width,
                        self.screen_height,
                        target.rect.center,
                        target_type,
                        target.direction
                    ))
                    # Clear drop zone if paratrooper killed on ground
                    if target_type == 'paratrooper' and target.on_ground:
                        self.zones.clear_zone(target.rect.centerx,
                                              self.current_player)
                    # Clear flight course for destroyed jets & helicopters
                    if target_type in ['jet', 'helicopter']:
                        self.waves[self.current_player].clear_course(
                            target.direction.x, target.flight_level)
                    # Remove target and update score
                    self.scores[self.current_player] += score
                    target_list.remove(target)
                    return True
                # Check for chute destruction
                if target_type == 'paratrooper' and target.under_canopy:
                    if sprite.collide_mask(projectile, target.chute):
                        self.sounds.play("fall")
                        target.sever_parachute()
                        return True
        return False

    def demolish_bunker(self, x_coords):
        """Animate the demolishing of the bunker.

        Args:
            x_coords([int]): List of paratrooper X coordinates
        """
        # Determine if attack is on the left side (True) or right side (False)
        right_x = self.zones.centers[self.zones.first_right]
        side = 'left' if x_coords[0] < right_x else 'right'
        if side == 'left':
            x_dir = 2
        else:
            x_dir = -2
        y = self.board.ground_y
        targets = self.zones.get_demo_targets(side, y, CROUCHED_SIZE)
        paratroopers = self.paratroopers[self.current_player]
        # Move 3 paratroopers to form pyramid
        for i in range(3):
            paratrooper = next(p for p in paratroopers
                               if p.rect.centerx == x_coords[i])
            paratrooper.current_sprite_index = 0 if side == "left" else 2
            gc.collect()
            for _ in range(x_coords[i], targets[i][0] + x_dir, x_dir):
                paratrooper.walk((x_dir, 0))
                self.clock.tick(self.fps * 2)
                self.render()
                display.flip()
            for _ in range(y, targets[i][1], -1):
                paratrooper.walk((0, -1))
                self.clock.tick(self.fps * 2)
                self.render()
                display.flip()
            paratrooper.crouch()
        # Move final paratrooper to demolish position
        paratrooper = next(p for p in paratroopers
                           if p.rect.centerx == x_coords[3])
        paratrooper.current_sprite_index = 4  # Bomb carrier
        gc.collect()
        for x in range(x_coords[3], targets[3][0] + x_dir, x_dir):
            paratrooper.walk((x_dir, 0))
            self.clock.tick(self.fps * 2)
            self.render()
            display.flip()
            if (x == targets[1][0] or x == targets[1][0] + 1 or
                    x == targets[2][0] or x == targets[2][0] + 1):
                # Climb up
                for _ in range(0, CROUCHED_SIZE[1]):
                    paratrooper.walk((0, -1))
                    self.clock.tick(self.fps * 2)
                    self.render()
                    display.flip()
        paratrooper.crouch()
        self.demolition_stage = Demolition.NONE
        self.bunker_destroyed = True
        self.explode_bunker()

    def explode_bunker(self):
        """Explode player's bunker."""
        self.sounds.play("destroy")  # Play destroy bunker sound
        self.explosions.append(Explosion(
            self.screen_width,
            self.screen_height,
            self.turret.center,
            "turret",
            (0, -12)
        ))

    def handle_input(self):
        """Handle keyboard and mouse input."""
        mouse_x, mouse_y = None, None
        for e in event.get():
            if (e.type == QUIT or e.type == KEYDOWN and
                    e.key == self.key_exit):
                quit()
                exit()
            if e.type == END_SOUND_EVENT:
                self.sounds.clean_up_channels()  # Clean up all unused channels
            if (self.bunker_destroyed or
                    self.demolition_stage == Demolition.ACTIVE):
                return
            if e.type == KEYDOWN:
                # Check current player fire input
                player_key = f"Player{self.current_player + 1}"
                if e.key == self.input_keys[player_key]["button1"]:
                    # Fire gun
                    self.sounds.play("fire")
                    if self.turret.animation_index == 0:
                        self.turret.animation_index += 1
                    self.bullets.append(
                        Bullet(self.turret.get_muzzle_pos(),
                               self.turret.get_muzzle_vector()))
                    self.scores[self.current_player] = max(
                        0, self.scores[self.current_player] - BULLET_PENALTY)

                # Check for mouse directional control
                for direction in ["left", "right"]:
                    if e.key == self.input_keys[player_key][direction]:
                        self.turret.move_keyboard(direction)

            if self.mouse_rel and e.type == MOUSEMOTION:
                mouse_x, mouse_y = e.rel  # Relative mouse movement

        if not self.mouse_rel:
            mouse_x, mouse_y = mouse.get_pos()  # Actual mouse position

        if (self.current_player == 0 and mouse_x and
                self.turret.mouse != mouse_x):
            self.turret.move(mouse_x, self.mouse_rel)
        elif (self.current_player == 1 and mouse_y and
              self.turret.mouse != mouse_y):
            self.turret.move(mouse_y, self.mouse_rel)

    def regulate_aircraft(self):
        """Generate helicopters and jets."""
        if self.waves[self.current_player].sorties <= 0:
            return
        if self.bunker_destroyed or self.demolition_stage != Demolition.NONE:
            return
        # Pause minimum 1 second between aircrafts
        self.frames_since_last_aircraft += 1
        if self.frames_since_last_aircraft < self.fps:
            return
        # Average number of frames between activations
        avg_frames = self.fps * self.waves[self.current_player].average_delay
        # Check if the random event should be activated
        if randint(0, int(avg_frames) - 1) == 0:
            add_chopper = True if (
                len(self.helicopters) <
                self.waves[self.current_player].max_helicopters) else False
            add_jet = True if (
                len(self.jets) <
                self.waves[self.current_player].max_jets) else False
            # Only allow 1 aircraft at a time (Either chopper or jet)
            if add_chopper and add_jet:
                if randint(0, 1):
                    add_chopper = False
                else:
                    add_jet = False

            if add_chopper or add_jet:
                dir_x, f_level = self.waves[self.current_player].get_course()
                self.frames_since_last_aircraft = 0
                self.waves[self.current_player].sorties -= 1

            if add_chopper:  # Add chopper
                drops = self.zones.get_drops(
                    self.waves[self.current_player].max_drops)
                self.helicopters.add(
                        Helicopter(screen_width=self.screen_width,
                                   drops=drops,
                                   direction_x=dir_x,
                                   flight_level=f_level))
            if add_jet:  # Add jet
                self.jets.add(
                        Jet(screen_width=self.screen_width,
                            direction_x=dir_x,
                            flight_level=f_level,
                            bunker_rect=self.board.bunker_rect),)
                if dir_x > 0:
                    self.sounds.loop("jet_lr", "play", False)
                else:
                    self.sounds.loop("jet_rl", "play", False)

    def render(self):
        """Render game elements."""
        self.screen.fill("skyblue4")  # Background color
        self.board.draw(self.screen)  # Game board
        self.board.draw_score(self.scores, self.lives, self.screen,
                              self.current_player)
        for bomb in self.bombs:
            bomb.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for explosion in self.explosions:
            explosion.draw(self.screen)
        for paratrooper in self.paratroopers[self.current_player]:
            paratrooper.draw(self.screen)
        if not self.bunker_destroyed:
            self.turret.draw(self.screen)
        self.helicopters.draw(self.screen)
        self.jets.draw(self.screen)
        # Display optional FPS
        if self.show_fps:
            self.board.draw_fps(self.screen, self.clock)
        # Check for cocktail mode
        if self.cocktail and self.current_player == 1:
            # Rotate the entire display by 180 degrees
            rotated_screen = transform.rotate(self.screen, 180)
            self.screen.blit(rotated_screen, (0, 0))

    def reset(self):
        """Reset game."""
        self.frames_since_last_aircraft = 255  # No delay at wave start
        self.lives = []
        self.paratroopers = {}
        if hasattr(self, 'scores'):  # Use current scores if resuming
            scores = self.scores
        else:
            scores = (0, ) * self.options.players
        self.scores = []
        if hasattr(self, 'waves'):  # Use current wave numbers if resuming
            wave_numbers = [wave.wave_number for wave in self.waves.values()]
        else:
            wave_numbers = (1, ) * self.options.players
        self.waves = {}
        for i in range(self.options.players):
            self.lives.append(self.total_lives - 1)
            self.paratroopers[i] = []
            self.scores.append(scores[i])
            wave_number = wave_numbers[i]
            self.waves[i] = Waves(wave_number)
            self.zones.clear_all_zones(player_id=i)
        self.current_player = 0

    def run(self):
        """Run game."""
        while True:
            self.clock.tick(self.fps)
            self.regulate_aircraft()
            self.handle_input()
            self.update()
            self.render()
            display.flip()
            self.collision_detection()

    def screen_complete(self):
        """Return True if screen clear of moving objects."""
        if (
                len(self.helicopters) == 0 and
                len(self.jets) == 0 and
                len(self.bombs) == 0 and
                len(self.explosions) == 0 and
                len(self.bullets) == 0):
            if (len(self.paratroopers[self.current_player]) == 0 or
                    all(p.state == Status.LANDED
                        for p in self.paratroopers[self.current_player])):
                return True
        return False

    def toggle_players(self):
        """Toggle current player."""
        if self.options.players < 2:
            return
        if self.current_player == 0 and self.lives[1] >= 0:
            self.current_player = 1
        elif self.current_player == 1 and self.lives[0] >= 0:
            self.current_player = 0

    def update(self):
        """Update turret, bullets, enemies."""
        # Check for next wave
        if (self.waves[self.current_player].sorties <= 0
                and self.screen_complete()):
            self.waves[self.current_player].next()
            # Switch players if 2 player game and bunker okay
            if (not self.bunker_destroyed and
                    self.demolition_stage == Demolition.NONE):
                self.toggle_players()
                self.render()
                self.board.display_wave_number(
                    self.waves[self.current_player].wave_number,
                    self.current_player, self.cocktail, self.screen, display)
                self.frames_since_last_aircraft = 255  # No delay at wave start
                gc.collect()
        # Check for destroyed bunker
        if self.bunker_destroyed and self.screen_complete():
            self.bunker_destroyed = False
            self.demolition_stage = Demolition.NONE
            self.paratroopers[self.current_player].clear()
            self.zones.clear_all_zones(self.current_player)
            self.turret.clear_animation()
            self.lives[self.current_player] -= 1
            if all(life < 0 for life in self.lives):
                self.board.game_over(
                    self.waves[self.current_player].wave_number,
                    self.screen, display)
                self.reset()
                self.render()
            self.toggle_players()
            self.render()
            # Display wave number and get ready
            self.board.display_wave_number(
                self.waves[self.current_player].wave_number,
                self.current_player, self.cocktail,
                self.screen, display, delay=3500)
            event.clear()  # Clear any keyboard events pressed during explosion
            self.frames_since_last_aircraft = 255  # No delay at wave start
            gc.collect()
        # Check for pending demoltion
        if (self.demolition_stage == Demolition.PENDING and
                self.screen_complete()):
            # Begin demoltion animation
            team_x = self.zones.get_demo_team(self.current_player)
            if team_x is None:
                # No longer 4 paratroopers on a side
                self.demolition_stage = Demolition.NONE
            else:
                # Begin demoltion
                self.demolition_stage = Demolition.ACTIVE
                self.demolish_bunker(team_x)
                return

        for bomb in self.bombs:
            if bomb.rect.bottom >= self.board.bunker_rect.top:
                self.bombs.remove(bomb)
                # Bunker destroyed by bomb
                self.bunker_destroyed = True
                self.explode_bunker()
            else:
                bomb.update()
        for bullet in self.bullets:
            bullet.update()
            x, y = bullet.location
            if x < 0 or x >= self.screen_width or y < 0:
                self.bullets.remove(bullet)

        for explosion in self.explosions:
            explosion.update()
            if explosion.count == 0:  # Check if exploding pieces gone
                self.explosions.remove(explosion)

        for helicopter in self.helicopters:
            drop_zone_x = helicopter.update()
            if drop_zone_x is not None:
                self.paratroopers[self.current_player].append(Paratrooper(
                    drop_zone_x,
                    self.zones.over_bunker(drop_zone_x),
                    helicopter.flight_level,
                    self.waves[self.current_player].max_flight_level,
                    ground_y=self.board.ground_y,
                    bunker_y=self.board.bunker_rect.top))
            if helicopter.out_of_bounds:  # Check if chopper exited screen
                self.waves[self.current_player].clear_course(
                    *helicopter.course)  # Clear course
                self.helicopters.remove(helicopter)  # Remove chopper
        # Helicopter sound effect
        if len(self.helicopters):
            if not self.sounds.loop_playing("helicopter"):
                self.sounds.loop("helicopter", "play")
        else:
            if self.sounds.loop_playing("helicopter"):
                self.sounds.loop("helicopter", "fadeout")

        for jet in self.jets:
            bomb_dropped = jet.update()
            if bomb_dropped:
                self.bombs.append(Bomb(jet.rect.midbottom, jet.direction))
                self.sounds.loop("bomb", "play", loop=False)

            if jet.out_of_bounds:  # Check if jet exited screen
                self.waves[self.current_player].clear_course(*jet.course)
                self.jets.remove(jet)  # Remove jet
        # Jet sound effects
        if not any(j.direction.x > 0 for j in self.jets):
            if self.sounds.loop_playing("jet_lr"):
                self.sounds.loop("jet_lr", "fadeout")
        if not any(j.direction.x < 0 for j in self.jets):
            if self.sounds.loop_playing("jet_rl"):
                self.sounds.loop("jet_rl", "fadeout")
        # Bomb sound effects
        if not len(self.bombs):
            if self.sounds.loop_playing("bomb"):
                self.sounds.loop("bomb", "fadeout")

        for paratrooper in self.paratroopers[self.current_player]:
            landing = paratrooper.update()
            if landing == Landing.DEAD:
                self.sounds.play("splat")
                self.scores[self.current_player] += PARATROOPER_SCORE
                hazardous = self.zones.is_occupied(paratrooper.rect.centerx,
                                                   self.current_player)
                self.explosions.append(Explosion(
                    self.screen_width,
                    self.screen_height,
                    paratrooper.rect.center,
                    "paratrooper",
                    0,
                    hazardous
                ))
                self.paratroopers[self.current_player].remove(paratrooper)
            elif landing == Landing.ON_BUNKER:
                # Bunker destroyed by single paratrooper landing on bunker
                self.bunker_destroyed = True
                self.demolition_stage == Demolition.NONE
                self.explode_bunker()
            elif landing == Landing.ON_GROUND:
                # Paratrooper safely landed
                ground_x = self.zones.set_occupied(paratrooper.rect.centerx,
                                                   self.current_player)
                if ground_x is None:
                    # Remove paratrooper if no room left on ground
                    self.paratroopers[self.current_player].remove(paratrooper)
                else:
                    paratrooper.rect.centerx = ground_x  # Unoccupied position
                # Check if 4 or more paratroopers have landed on a side
                if (self.zones.critical(self.current_player)
                        and not self.bunker_destroyed):
                    # Bunker destroyed by 4 paratroopers landing on a side
                    self.demolition_stage = Demolition.PENDING


if __name__ == "__main__":
    while True:
        game = Game()
        game.run()
