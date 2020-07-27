# Expendibots
This repository contains two game-playing agents (1, 2) as well as functionality for a human user to play (3):
1. `AI`     -- an exploration of:
  - mtd-f algorithm
  - transposition table with LRU algorithm
  - move prioritisation
  - iterative deepening with both time-based and PV-Nodes games-over cut-off
  - Hardcoded strategy for opening four-moves of game
2. `randm`  -- a simple agent that chooses randomly from its available actions
3. `human`  -- a simple player that chooses actions according to user input, i.e. a human player

## Rules of the game
Expendibots is a novel 8x8 board game, whose rules are explained in detail [here](https://github.com/naughtona/expendibots-game-engine/game-rules.pdf).

## Project specification
This repository is an extension of one of the projects I was set in COMP30024 Artificial Intelligence (University of Melbourne) in Semester One, 2020.

The project specification can be found [here](https://github.com/naughtona/expendibots-game-engine/project-spec.pdf). 

## `AI` Game-Playing Agent
A write-up of the strategy and thought-processes behind the AI Game-Playing Agent can be found [here](https://github.com/naughtona/expendibots-game-engine/report.pdf).

## Usage
After cloning, run:
```bash
cd expendibots-game-engine
```

Now that you are in the root directory, you can invoke the game by specifying two agents as follows:
```bash
python3 -m referee <white package> <black package>
```

## Examples
To play `AI` against `randm`, run:
```bash
python3 -m referee AI randm
```

To play against the `AI` as `human`, run:
```bash
python3 -m referee AI human
```

To play against `randm` as `human`, run:
```bash
python3 -m referee randm human
```

## Acknowledgements
The referee package has been supplied by and belongs to the COMP30024 teaching staff.

# License
[MIT](https://choosealicense.com/licenses/mit/)
