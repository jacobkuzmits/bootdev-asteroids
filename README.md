# Asteroids

Asteroids is a small arcade-style game built with [Pygame](https://www.pygame.org/) as a course for boot.dev. Pilot a triangular ship, blast incoming asteroids, and chase a high score while juggling limited lives.

## Requirements

- Python 3.13 or newer
- `pygame==2.6.1`
- (Optional) [uv](https://docs.astral.sh/uv/) for dependency management and running the project

## Setup & Run

### Option 1: Using uv

1. Install uv following the instructions for your platform.
2. In the project directory, install dependencies and run the game:
   ```bash
   uv run main.py
   ```

### Option 2: Using python / pip

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install the required dependency:
   ```bash
   pip install pygame==2.6.1
   ```
3. Start the game:
   ```bash
   python main.py
   ```

## Controls

- `W` / `S`: Thrust forward / backward
- `A` / `D`: Rotate left / right
- `Space`: Fire shots

Avoid collisions, split asteroids into smaller pieces, and rack up points. You begin with three lives—once you lose them, your score is recorded and you return to the main menu.

## Project Notes

- `main.py` serves as the entry point and manages the game loop, menus, and HUD.
- Supporting modules define the player ship, asteroids, collision logic, and shared constants.
- The code is distributed under the terms of the included `LICENSE`.
