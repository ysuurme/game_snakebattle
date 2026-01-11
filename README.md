🚀 **Game Snake Battle:** A competitive, object-oriented implementation of the classic snake game.

A competitive local multiplayer simulation built with Pygame to apply grid-based coordinate logic and data structures, or in plain language, to manage dynamic snake bodies and collision detection on a shared grid. This project combines real-time event handling and game state updates through a modular Object-Oriented Architecture."

![Project Demo](assets/game_snakebattle_lowres.gif)

🛠️ **Skills & Learning Overview:** This project served as a practical application of several core software engineering concepts:

*   **Modular Architecture:** The /src or Source folder models complex systems like the Game Loop (`Game`) and Entity Attributes (`Snake`) and (`Snack`) into distinct classes and files. I evolved the game fundamentals with immutable dataclasses for game state and snake coordination.
*   **Mathematical Game Coordination:** Implements arithmetic logic to map logical grid coordinates (Rows/Cols) to screen positions (X/Y) for accurate rendering of the game.
*   **Event-Driven Programming:** Manages a real-time game loop to handle user input (mouse clicks) and game events seamlessly.

⚡ **Fast-Track Setup:**
Get up and running in seconds with `uv`:

```bash
uv sync
uv run main.py
```

📋 **Project Glossary:**
A classic game in a jolly color scheme. This project is inspired by the Object Oriented Programming tutorial of 'Tech with Tim'.

* ["Snake Pygame"](https://www.youtube.com/watch?v=5tvER0MT14s&t=1s) - *Tech With Tim*

🎮 **Controls:**
The hunt is for a typical Dutch treat "d'n Bossche Bol"

| Player | Up | Down | Left | Right |
| :--- | :---: | :---: | :---: | :---: |
| **Player 1** | `↑` | `↓` | `←` | `→` |
| **Player 2** | `W` | `S` | `A` | `D` |

> Press **`ESC`** to quit the game.

*Future aim will be to play against an AI with custom difficulty