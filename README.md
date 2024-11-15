
# Who Asked?
A small terminal simulation with event-driven programming

---

*“I moved!”  
“Who…?!”  
“Me!”  
“…Who asked?!”*

---

Welcome to **Who Asked?**, a small terminal-based simulation designed to demonstrate event-driven programming in Python. The project is a study tool created to help understand how an event-driven architecture could be implemented in a simple game-like environment.

This program simulates a game world where players and enemies move around a grid, interacting through events triggered by actions like movement or collisions. The system is built around the principles of **event-driven programming**, which means that the game reacts to events, with each event triggering a response from listeners.

---

## About the Code

This code was originally written in 2019 as a learning project. I recently translated it from Portuguese to English and refactored it to improve readability and security. The goal of this project was to understand how an event-driven architecture could work in Python, using a basic game as an example. While refactoring, I tried to preserve the original structure and logic of the program to maintain its educational purpose.

---

## How it works

In **Who Asked?**, events like player movement or enemy actions trigger certain changes in the simulation. The event-driven nature of the game allows for dynamic behavior where actions are only taken when specific conditions are met. 

---

## Key Parameters

The game includes several parameters to adjust the game’s settings and difficulty:

- **Enemies count**: Defines the number of enemies in the game.
- **Map width**: The width of the playing field.
- **Map height**: The height of the playing field.
- **Survival Factor**: This parameter affects the overall difficulty of the game. A higher value makes the game easier, while a lower value increases the difficulty. It's not a direct “chance to win” but rather a factor that influences the player’s chances of surviving or succeeding.
- **Sleep time**: The time between game updates, controlling the speed of the game.

---

## How to Run

To run the simulation, execute the following command in your terminal:

```bash
python game.py <enemies_count> <map_width> <map_height> <survival_factor> <sleep_time>
```

For example:

```bash
python game.py 10 10 10 50 250
```

This will start the game with 10 enemies, a 10x10 map, a survival factor of 50, and a game speed controlled by a 250 millisecond interval.

---

Feel free to fork, modify, or experiment with the project as you like. This project is meant for learning purposes and to demonstrate how event-driven programming can be applied in a simple, game-like scenario.
