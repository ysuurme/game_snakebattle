🚀 **Game Snake Battle:** A competitive, object-oriented implementation of the classic snake game.

A competitive local multiplayer simulation built with Pygame to apply grid-based coordinate logic and data structures, or in plain language, to manage dynamic snake bodies and collision detection on a shared grid. This project combines real-time event handling and game state updates through a modular Object-Oriented Architecture."

![Project Demo](assets/game_snakebattle_lowres.gif)

🛠️ **Skills & Learning Overview:** This project served as a practical application of several core software engineering concepts:

*   **Modular Architecture:** The /src or Source folder models complex systems like the Game Loop (`Game`) and Entity Attributes (`Snake`) and (`Snack`) into distinct classes and files. I evolved the game fundamentals with immutable dataclasses for game state and snake coordination. 
*   **Dynamic Players:** The Game now supports variable player configurations (Single, Player vs Player, Player vs AI Agent).
*   **AI Infrastructure:** Implemented a Deep Q-Network (DQN) using PyTorch Linear_QNet. Created Trainer and Agent in src/ai to handle the reinforcement learning loop (State -> Action -> Reward -> Train).
*   **Event-Driven Programming:** Manages a real-time game loop through run() and play_step() to handle user input (keyboard) and AI Agent control

⚡ **Fast-Track Setup:**
Get up and running in seconds with `uv`:

```bash
uv sync
uv run main.py
```

📋 **Project Glossary:**
A classic game in a jolly color scheme. This project is inspired by the Object Oriented Programming tutorial of 'Tech with Tim'.

* ["Snake Pygame"](https://www.youtube.com/watch?v=5tvER0MT14s&t=1s) - *Tech With Tim*
* ["Train an AI to Play Snake"](https://www.youtube.com/watch?v=L8ypSXwyBds) - *Python + PyTorch + Pygame Reinforcement Learning*

🎮 **Controls:**
The hunt is for a typical Dutch treat "d'n Bossche Bol"

| Player | Up | Down | Left | Right |
| :--- | :---: | :---: | :---: | :---: |
| **Player 1** | `↑` | `↓` | `←` | `→` |
| **Player 2** | `W` | `S` | `A` | `D` |

| Game Modes |
| :--- |
| Single Player: Solo practice mode |
| Player vs Player: Classic WASD vs Arrows |
| Player vs Agent: Play against your trained AI model! |
| Agent Training: Watch the AI learn in real-time with live plotting |
> Press **`ESC`** to quit the game.
