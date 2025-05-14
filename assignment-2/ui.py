#!/usr/bin/env python3
"""
ui.py: Rendering module for Dr. Mario terminal game.
"""

from game_logic import Virus, CapsuleSegment


class Renderer:
    """Handles printing the game field to the terminal in the required format."""
    def __init__(self, game_state):
        self.game = game_state

    def render(self):
        rows = self.game.rows
        cols = self.game.cols
        # Build a text matrix initialized with empty cells
        display = [[ '   ' for _ in range(cols)] for _ in range(rows)]

        # Fill in static grid cells
        for r in range(rows):
            for c in range(cols):
                cell = self.game.grid[r][c]
                if cell is None:
                    continue
                if isinstance(cell, Virus):
                    # Virus: lowercase letter centered
                    display[r][c] = f' {cell.color} '
                elif isinstance(cell, CapsuleSegment):
                    # Capsule segment: horizontal vs vertical
                    if cell.orientation == 'horizontal':
                        if cell.part == 'left':
                            display[r][c] = f' {cell.color}-'
                        else:
                            display[r][c] = f'-{cell.color} '
                    else:
                        # vertical capsule segment: single piece
                        display[r][c] = f' {cell.color} '

        # Overlay current faller if one exists
        faller = self.game.faller
        if faller:
            for idx, (r, c, color) in enumerate(faller.positions()):
                # Skip if out of bounds
                if not (0 <= r < rows and 0 <= c < cols):
                    continue
                if faller.state == 'falling':
                    if faller.orientation == 'horizontal':
                        # left vs right end
                        disp = f'[{color}-' if idx == 0 else f'-{color}]'
                    else:
                        # vertical falling
                        disp = f'[{color}]'
                else:
                    # landed but not frozen
                    if faller.orientation == 'horizontal':
                        disp = f'|{color}-' if idx == 0 else f'-{color}|'
                    else:
                        disp = f'|{color}|'
                display[r][c] = disp

        # Print each row with boundaries
        for r in range(rows):
            print('|' + ''.join(display[r]) + '|')

        # Print bottom border
        print(' ' + '-' * (cols * 3) + ' ')
