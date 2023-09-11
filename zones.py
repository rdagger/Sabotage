"""Drop Zones."""
from random import random, randint, sample


class Zones:
    """Drop zones designate X positions where paratroopers can jump."""

    def __init__(self, screen_width, bunker_width, players, zone_width=29):
        """Initialize zones.

        Args:
            screen_width(int): Overall screen width of game
            bunker_width(int): Width of bunker
            players(int): Total number of players
            zone_width(int): Width of drop zones
        """
        self.screen_width = screen_width
        self.bunker_width = bunker_width
        self.zone_width = zone_width
        self.centers = {}  # Dict - key=zone #, value=center X
        self._create_zones()
        self.occupied = {}  # Paratrooper occupied zones per player
        for player in range(players):  # Organize by left & right of bunker
            self.occupied[player] = {'left': [], 'right': []}

    def clear_all_zones(self, player_id):
        """Remove paratroopers from all occupied zone per player.

        Args:
            player_id(int): Player ID
        """
        self.occupied[player_id]['left'].clear()
        self.occupied[player_id]['right'].clear()

    def clear_zone(self, x, player_id):
        """Remove paratrooper from occupied zone.

        Args:
            x(int):  Paratrooper center X coordinate
            player_id(int): Player ID
        """
        zone = next((key for key, value in self.centers.items()
                     if value == x), None)
        if zone is None:
            return
        elif zone >= self.first_right:
            self.occupied[player_id]['right'].remove(zone)
        elif zone > 2:
            self.occupied[player_id]['left'].remove(zone)

    @property
    def count(self):
        """Return total number of drop zones."""
        return len(self.centers)

    def _create_zones(self):
        """Generate a dict of the drop zone centers."""
        bunker_left_edge = self.screen_width / 2 - self.bunker_width / 2
        bunker_right_edge = self.screen_width / 2 + self.bunker_width / 2
        zone_counter = 3  # Start with zone 3

        # Zones to the left of the bunker with buffer zone
        x = bunker_left_edge - 2 * self.zone_width  # Bunker buffer
        while x >= self.zone_width:  # Screen left buffer
            center_x = round((x + x + self.zone_width) / 2)
            self.centers[zone_counter] = center_x
            zone_counter += 1
            x -= self.zone_width

        # Store starting right zone
        self.first_right = zone_counter

        # Zones inside bunker (1 on each outside edge)
        x = bunker_left_edge
        center_x = round((x + x + self.zone_width) / 2)
        self.centers[1] = center_x

        x = bunker_right_edge - self.zone_width
        center_x = round((x + x + self.zone_width) / 2)
        self.centers[2] = center_x

        # Zones to the right of the bunker with buffer zone
        x = bunker_right_edge + self.zone_width  # Bunker buffer
        while x + 2 * self.zone_width <= self.screen_width:  # Right buffer
            center_x = round((x + x + self.zone_width) / 2)
            self.centers[zone_counter] = center_x
            zone_counter += 1
            x += self.zone_width

    def critical(self, player_id):
        """Returns True if left or rights zones have 4 paratroopers or more.

        Args:
            player_id(int): Player ID
        """
        return (len(self.occupied[player_id]['left']) >= 4 or
                len(self.occupied[player_id]['right']) >= 4)

    def get_demo_team(self, player_id):
        """Get the X locations of the 4 closest paratroopers on a side.

        Args:
            player_id(int): Player ID
        """
        if len(self.occupied[player_id]['left']) >= 4:
            # Get 4 closest zones on left to bunker
            left = sorted(self.occupied[player_id]['left'])[:4]
            # Return zone X coordinates
            return [self.centers[key] for key in left]
        elif len(self.occupied[player_id]['right']) >= 4:
            # Get 4 closest zones on right to bunker
            right = sorted(self.occupied[player_id]['right'])[:4]
            # Return zone X coordinates
            return [self.centers[key] for key in right]
        else:
            return None

    def get_demo_targets(self, side, paratrooper_y, crouched_size):
        """Get the locations of the target locations for attack.

        Args:
            side(string): Left or right side
            paratrooper_y(int): Y coordinte for ground level paratroopers
            crouched_size([int, int]): Width & height of a crouched paratrooper
        """
        targets = []
        width, height = crouched_size
        if side == 'left':
            # Left side
            targets.append((self.centers[3] + width, paratrooper_y))
            targets.append((self.centers[3] + width, paratrooper_y -
                            height))
            targets.append((self.centers[3], paratrooper_y))
            targets.append((self.centers[3] + width, paratrooper_y -
                           (height * 2)))
        else:
            # Right side
            targets.append((self.centers[self.first_right] - width,
                            paratrooper_y))
            targets.append((self.centers[self.first_right] - width,
                            paratrooper_y - height))
            targets.append((self.centers[self.first_right], paratrooper_y))
            targets.append((self.centers[self.first_right] - width,
                            paratrooper_y - (height * 2)))
        return targets

    def get_drops(self, max_drops):
        """Get a list of drop zones based on the maximum drops.

        Args:
            max_drops(int): The maximum number of drops
        """
        if random() >= .25:  # 25% of choppers don't drop paratroopers
            if max_drops > 0:
                drop_count = randint(1, max_drops)
                return sample(list(self.centers.values()), drop_count)
        return []

    def is_occupied(self, x, player_id):
        """Return if zone is occupied by a landed paratrooper.

        Args:
            x(int):  Paratrooper center X coordinate
            player_id(int): Player ID
        """
        zone = next((key for key, value in self.centers.items()
                     if value == x), None)
        if zone is None:
            return False
        elif zone >= self.first_right:
            return zone in self.occupied[player_id]['right']
        else:
            return zone in self.occupied[player_id]['left']

    def set_occupied(self, x, player_id):
        """Designate a zone occupied by paratrooper.

        Args:
            x(int):  Zone center X coordinate
            player_id(int): Player ID
        Returns:
            int: X coordinate of occupied zone
        """
        zone = next(key for key, value in self.centers.items() if value == x)
        if zone >= self.first_right:
            # Right of bunker
            if zone not in self.occupied[player_id]['right']:
                self.occupied[player_id]['right'].append(zone)
                return self.centers[zone]
            # If the zone is in the list, find the closest available zone
            increment = 1
            while True:
                # Check higher number
                if (zone + increment <= self.count and zone +
                        increment not in self.occupied[player_id]['right']):
                    self.occupied[player_id]['right'].append(zone + increment)
                    return self.centers[zone + increment]
                # Check lower number
                if (zone - increment >= self.first_right and zone -
                        increment not in self.occupied[player_id]['right']):
                    self.occupied[player_id]['right'].append(zone - increment)
                    return self.centers[zone - increment]
                increment += 1
                if increment > self.count:
                    # Zones all full
                    return None
        else:
            # Left of bunker
            if zone not in self.occupied[player_id]['left']:
                self.occupied[player_id]['left'].append(zone)
                return self.centers[zone]
            # If the zone is in the list, find the closest available zone
            increment = 1
            while True:
                # Check higher number
                if (zone + increment < self.first_right and zone +
                        increment not in self.occupied[player_id]['left']):
                    self.occupied[player_id]['left'].append(zone + increment)
                    return self.centers[zone + increment]
                # Check lower number
                if (zone - increment >= 3 and zone -
                        increment not in self.occupied[player_id]['left']):
                    self.occupied[player_id]['left'].append(zone - increment)
                    return self.centers[zone - increment]
                increment += 1
                if increment > self.count:
                    # Zones all full
                    return None

    def over_bunker(self, x):
        """Determine if zone center X is over bunker.

        Args:
            x(int):  Zone center X coordinate.
        """
        zone = next(key for key, value in self.centers.items() if value == x)
        return True if zone <= 2 else False
