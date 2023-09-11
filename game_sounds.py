"""Game sounds."""
from pygame import mixer, USEREVENT
from os import path

END_SOUND_EVENT = USEREVENT + 1

SOUND_EFFECTS = ['bomb', 'destroy', 'explode', 'fall', 'fire', 'helicopter',
                 'jet_lr', 'jet_rl', 'parachute', 'shot', 'splat']


class GameSounds():
    """Generates, loads and plays sounds."""

    def __init__(self, volume=1.0):
        """Game sounds constructor.

        Args:
            volume(float): Volume 0 - 1.0 (Default 1.0)
        """
        mixer.init()
        mixer.set_num_channels(16)

        self.volume = volume
        self.sound_effects = {}
        self.used_channels = set()
        self.load_sound_effects()

    def clean_up_channels(self):
        """Clean up any finished channels."""
        for channel in list(self.used_channels):
            if not channel.get_busy():
                self.used_channels.remove(channel)

    def load_sound_effects(self):
        """Load all game sound effects."""
        for effect in SOUND_EFFECTS:
            self.sound_effects[effect] = mixer.Sound(path.join("sounds",
                                                     effect + ".mp3"))

    def loop_playing(self, effect):
        """Return if looped sound effect playing.

        Args:
            effect(string): Effect to play.
        """
        for channel in list(self.used_channels):
            if channel.get_sound() == self.sound_effects[effect]:
                return channel.get_busy()
        return False

    def loop(self, effect, cmd="play", loop=True):
        """Control sounds with optional repeating loop.

        Args:
            effect(string): Effect to play.
            cmd(string): fadeout, play or stop
            loop(bool): Repeat sound
        """
        if loop:
            loop_set = -1
        else:
            loop_set = 0

        if cmd == "play":
            channel = mixer.find_channel()
            if channel is None:  # Do not play if no channels available
                return
            self.used_channels.add(channel)
            channel.play(self.sound_effects[effect], loops=loop_set)
            channel.set_endevent(END_SOUND_EVENT)
        elif cmd == "stop":
            # Stop and free up all channels playing the effect.
            for channel in list(self.used_channels):
                if channel.get_sound() == self.sound_effects[effect]:
                    channel.stop()
                    self.used_channels.remove(channel)
        elif cmd == "fadeout":
            # Fadeout and free up all channels playing the effect.
            for channel in list(self.used_channels):
                if channel.get_sound() == self.sound_effects[effect]:
                    channel.fadeout(500)
                    self.used_channels.remove(channel)

    def play(self, effects, pause=False):
        """Play sound effect(s).

        Args:
            effects(string or [string]): Effect(s) to play.
            pause(bool): True to pause until sound is played
        """
        if isinstance(effects, str):  # Handle single effect
            effects = [effects]
        # Play effect(s)
        for effect in effects:
            channel = mixer.find_channel()
            if channel is None:  # Do not play if no channels available
                return
            self.used_channels.add(channel)
            channel.play(self.sound_effects[effect])
            channel.set_endevent(END_SOUND_EVENT)
            if pause:
                while channel.get_busy():
                    continue
