"""Attack Waves."""
from random import choice, randint

"""WAVES contains the difficulty settings for each wave:
    max_helicopters: Maximum number of helicopters on screen at one time
    max_jets: Maximum number of jets on screen at one time
    max_flight_level: Higher for lower flying aircraft & lower chute deployment
    max_drops: Maximum number of paratroopers dropped per helicopter
    sorties: Total number of aircraft per wave
    speed: Aircraft speed (minimum 2, maximum 7)
    average_delay: Average delay between aircraft
"""
WAVES = {
    1: {"max_helicopters": 2, "max_jets": 0, "max_flight_level": 2,
        "max_drops": 2, "sorties": 6, "speed": 3, "average_delay": 1},
    2: {"max_helicopters": 3, "max_jets": 0, "max_flight_level": 3,
        "max_drops": 3, "sorties": 10, "speed": 4, "average_delay": 1.75},
    3: {"max_helicopters": 4, "max_jets": 0, "max_flight_level": 4,
        "max_drops": 3, "sorties": 10, "speed": 5, "average_delay": 1.5},
    4: {"max_helicopters": 0, "max_jets": 1, "max_flight_level": 1,
        "max_drops": 0, "sorties": 5, "speed": 4, "average_delay": 1.25},
    5: {"max_helicopters": 4, "max_jets": 0, "max_flight_level": 5,
        "max_drops": 3, "sorties": 10, "speed": 5, "average_delay": 1},
    6: {"max_helicopters": 0, "max_jets": 2, "max_flight_level": 3,
        "max_drops": 0, "sorties": 10, "speed": 5, "average_delay": 1},
    7: {"max_helicopters": 5, "max_jets": 0, "max_flight_level": 10,
        "max_drops": 0, "sorties": 25, "speed": 7, "average_delay": .2},
    8: {"max_helicopters": 4, "max_jets": 0, "max_flight_level": 6,
        "max_drops": 4, "sorties": 15, "speed": 5, "average_delay": 1},
    9: {"max_helicopters": 4, "max_jets": 0, "max_flight_level": 2,
        "max_drops": 12, "sorties": 15, "speed": 3, "average_delay": 1},
    10: {"max_helicopters": 5, "max_jets": 0, "max_flight_level": 7,
         "max_drops": 5, "sorties": 20, "speed": 6, "average_delay": 1},
    11: {"max_helicopters": 2, "max_jets": 3, "max_flight_level": 5,
         "max_drops": 4, "sorties": 20, "speed": 5, "average_delay": 1},
    12: {"max_helicopters": 5, "max_jets": 0, "max_flight_level": 7,
         "max_drops": 8, "sorties": 20, "speed": 3, "average_delay": .2},
    13: {"max_helicopters": 3, "max_jets": 3, "max_flight_level": 6,
         "max_drops": 4, "sorties": 20, "speed": 5, "average_delay": 1}
}


class Waves:
    """Attack waves."""

    def __init__(self, wave_number):
        """Wave constructor.

        Args:
            wave_number(int): Wave number to start on
        """
        self.max_helicopters = 0
        self.max_jets = 0
        self.max_flight_level = 0  # Flight levels measured from top of screen
        self.max_drops = 0
        self.sorties = 0
        self.speed = 0
        self.wave_number = wave_number
        self._load_wave()
        self.bands = {}  # Initialize flight bands
        self.clear_all_courses()

    def clear_all_courses(self):
        """Clear all courses from flight bands."""
        max_band = max(wave['max_flight_level'] for wave in WAVES.values())
        self.bands = {i: 0 for i in range(1, max_band + 1)}

    def clear_course(self, direction, flight_level):
        """Clear a course from the flight bands.

        Args:
            direction(int): Direction -1 or 1
            flight_level(int): Flight level from top of screen
        """
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1
        self.bands[flight_level] -= direction

    def get_course(self):
        """Get an initial direction and flight level."""
        flight_level = randint(1, self.max_flight_level)
        current_band_dir = 1 if self.bands[flight_level] > 0 else (
            -1 if self.bands[flight_level] < 0 else 0)

        if current_band_dir != 0:
            direction = current_band_dir  # Avoid collsions
        else:
            direction = choice([-1, 1])  # Left to right=1, Right to left=-1
        self.bands[flight_level] += direction
        return (direction * self.speed, flight_level)

    def next(self):
        """Set next wave."""
        self.wave_number += 1
        self._load_wave()

    def _load_wave(self):
        """Load the wave data."""
        if self.wave_number > len(WAVES):
            # Repeat last 2 waves when last wave reached.
            if self.wave_number % 2:
                wave_number = len(WAVES)
            else:
                wave_number = len(WAVES) - 1
        else:
            wave_number = self.wave_number
        # Populate instance variable from WAVES dict
        for key, value in WAVES[wave_number].items():
            setattr(self, key, value)
