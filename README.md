# Sabotage

This project is a Pygame remake of the classic Apple ][ game, Sabotage, originally developed by Mark Allen in 1981.

![Sabotage01](https://github.com/rdagger/Sabotage/assets/106355/48e3cbad-f220-4177-9914-3579ef90564f)

Overview

I developed this remake specifically for my vintage cocktail table arcade machine. While it's optimized for a 1024x1280 vertical monitor resolution, the game is compatible with other common resolutions as well. Configuration options such as resolution and control settings can be customized via the settings.ini file. Difficulty adjustments can be made by modifying the WAVES dictionary in waves.py.

Features

    Controls: Use the mouse or arrow keys to control the player's turret.
    Multiplayer Support: The game supports 1 or 2 players.
        Player 1: Turbo Twist spinner (X-axis)
        Player 2: Turbo Twist spinner (Y-axis)
        Single-player: Regular mouse
    Control Customization: Easily switch between relative motion and actual mouse position based on your input device.
    Customizable Keys: Default keys can be modified in settings.ini. Refer to pygame_keys.txt in the utils folder for key constants.

Gameplay

    Scoring: Earn points by destroying helicopters, paratroopers, jets, and bombs.
    Shrapnel Effect: Explosion shrapnel can take out other aircraft and paratroopers.
    Paratrooper Dynamics: Shoot parachutes to make a paratroopers fall. Free-falling paratroopers can eliminate those on the ground.
    Resource Management: Every bullet fired subtracts from your score, so aim and accuracy are crucial.
    Game Over Conditions:
        Four paratroopers land on one side of your bunker.
        A single paratrooper lands on the top of your bunker.
        A bomb lands on the turret.

Default Keyboard Controls

    Player 1 Button: Left CTRL
    Player 2 Button: A
    Movement Keys:
        Player 1: Left & Right Arrow keys
        Player 2: D & G

Dependencies

    Pygame

Legacy

The Sabotage concept has inspired various clones and remakes over the decades, including:

    Commando Raid (Atari 2600, 1982)
    Paratrooper (PC, 1982)
    Paratroop Attack (Atari 800, 1982)
    Airborne! (Macintosh, 1984)
    Green Paras (Atari 800, 1987)
    Night Raid (PC, 1992)
    Ack-Ack Attack! (PC & PalmOS, 1995)
    Ganja Farmer (PC, 1998)
    Parachute (iPod, 2001)

Contributing

Feel free to contribute to the project by submitting issues or pull requests.

License

This project is open-source, feel free to use it under the terms specified in the LICENSE file.

Enjoy the game!
