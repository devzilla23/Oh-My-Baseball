# Oh My Baseball

Oh My Baseball is a lightweight arcade-style batting game built with Python and Pygame. You start at the menu, choose a mode, and then time your swing as a pitch approaches the plate. Each hit adds distance, which contributes to your total and can be spent in the shop to improve your swing and overall performance.

## Preview

![Title screen](docs/title-screen.png)

![Gameplay](docs/gameplay.png)

## Features

- Single-player batting gameplay with timing-based swings
- Randomized pitch motion and ball flight
- Distance tracking in feet for each hit
- Foul detection and game-over flow after a limited number of pitches
- Persistent upgrades through the shop system
- Save data stored in JSON files for stats, progress, and shop costs

## How to run

1. Install Python 3.10+.
2. Install Pygame:

   ```bash
   python -m pip install pygame
   ```

3. From the project folder, start the game:

   ```bash
   python Oh_My_Baseball.py
   ```

## Controls

- `Space`: pitch the ball / swing at the plate
- Mouse click: select buttons in the title and shop screens
- Use the game loop to track your total distance and return to the menu after a game over

## Project structure

- `Oh_My_Baseball.py` — main game loop and mode switching
- `Data/playone.py` — pitch logic, swing timing, field behavior, scoring, and game UI
- `Data/TitleScreen.py` — title menu and buttons
- `Data/Shop.py` — upgrade system and saved progression
- `Data/Assets/sprites/` — game art and animations
- `Data/playerStats.json` — player upgrade stats
- `Data/playerFt.json` — total distance record
- `Data/costs.json` — shop upgrade cost values

## Notes

- This is a small local arcade game designed for quick play sessions.
- Progress is saved automatically through the JSON files in the `Data` folder.
- The shop upgrades improve batting, contact, pitch count, and distance potential over time.
