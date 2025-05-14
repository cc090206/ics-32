#!/usr/bin/env python3
"""
a2.py: Entry point for the Dr. Mario terminal game simulation.
Reads input, initializes game state, handles the main loop, and delegates
tasks to game_logic and ui modules.
"""
import sys

from game_logic import GameState
from ui import Renderer


def parse_initial_contents(game: GameState, rows: int) -> None:
    """
    Populate the game field if the initial mode is CONTENTS.
    Otherwise (EMPTY), leave the board blank.
    """
    mode = sys.stdin.readline().strip()
    if mode == 'CONTENTS':
        for r in range(rows):
            line = sys.stdin.readline().rstrip("\n")
            game.set_initial_row(r, line)
    # If mode == 'EMPTY', do nothing


def main():
    # Read field dimensions
    rows = int(sys.stdin.readline())
    cols = int(sys.stdin.readline())

    # Initialize game state
    game = GameState(rows, cols)
    parse_initial_contents(game, rows)

    # Renderer for printing the field
    renderer = Renderer(game)

    # Main game loop
    while True:
        # Print current field
        renderer.render()

        # Print LEVEL CLEARED if no viruses remain
        if game.level_cleared():
            print("LEVEL CLEARED")

        # Read the next command (blank line allowed)
        raw = sys.stdin.readline()
        if raw is None:
            break
        cmd = raw.rstrip("\n")

        # Quit command
        if cmd == 'Q':
            break

        # Advance one step on blank input
        if cmd == '':
            game.step()
        else:
            # Handle commands: F, V, A, B, <, >
            game.handle_command(cmd)
            # After creating a faller, check for game-over condition
            if game.is_game_over():
                renderer.render()
                print("GAME OVER")
                break


if __name__ == '__main__':
    main()
