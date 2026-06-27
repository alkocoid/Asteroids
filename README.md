# Asteroids

A Python/Pygame rebuild of the classic arcade game **Asteroids**, made as part of the Boot.dev learning path and extended with extra gameplay features.

## Features

- Player ship movement, rotation, and shooting
- Random asteroid spawning
- Asteroids split into smaller pieces when hit
- Score tracking based on asteroid size
- Lives and temporary invincibility after respawn
- Game over, restart, name entry, and top-10 leaderboard

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/) or another Python environment manager

## Setup

Install dependencies:

```bash
uv sync
```

## Run

Start the game:

```bash
uv run main.py
```

## Controls

| Key | Action |
| --- | --- |
| `W` | Thrust forward |
| `S` | Move backward |
| `A` | Rotate left |
| `D` | Rotate right |
| `Space` | Shoot |
| `Enter` | Start, restart, or submit score |
| `Esc` | Quit |

## Notes

Leaderboard scores are saved locally in `leaderboard.json`. Runtime log files and local leaderboard data are ignored by Git.
