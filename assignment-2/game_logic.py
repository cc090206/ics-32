import shlex
from collections import deque


class Virus:
    """Represents a single-cell virus of a given color."""
    def __init__(self, color):
        self.color = color


class CapsuleSegment:
    """Represents one segment of a frozen capsule, including connectivity."""
    def __init__(self, cap_id, color, orientation, part):
        # cap_id: identifier grouping two segments
        # orientation: 'horizontal' or 'vertical'
        # part: 'left'/'right' for horizontal, 'top'/'bottom' for vertical
        self.cap_id = cap_id
        self.color = color
        self.orientation = orientation
        self.part = part


class Faller:
    """Represents the current falling capsule (two segments)."""
    def __init__(self, color1, color2, mid_col):
        # color1 = left segment, color2 = right segment initially
        self.color1 = color1
        self.color2 = color2
        # 'horizontal' or 'vertical'
        self.orientation = 'horizontal'
        # 'falling', 'landed'
        self.state = 'falling'
        # origin position: if horizontal, left segment at (row, col)
        # if vertical, bottom segment at (row, col)
        self.row = 1  # always second row index
        self.col = mid_col

    def positions(self):
        """Return list of (r,c,color) for the two segments."""
        if self.orientation == 'horizontal':
            return [
                (self.row, self.col, self.color1),
                (self.row, self.col + 1, self.color2)
            ]
        else:  # vertical
            # top segment = color1, bottom = color2
            return [
                (self.row - 1, self.col, self.color1),
                (self.row, self.col, self.color2)
            ]

    def rotate(self, clockwise=True):
        """Toggle orientation; actual placement and kicks handled by GameState."""
        self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'


class GameState:
    """Encapsulates the game board, static pieces, and current faller."""
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # static grid: None, Virus, or CapsuleSegment
        self.grid = [[None] * cols for _ in range(rows)]
        self.faller = None
        self.next_cap_id = 1
        self.game_over = False

    def set_initial_row(self, r, line):
        """Populate static row r from a CONTENTS line of length cols."""
        for c, ch in enumerate(line):
            if ch in 'rby':
                self.grid[r][c] = Virus(ch)
            elif ch in 'RBY':
                # treat as single disconnected capsule half
                self.grid[r][c] = CapsuleSegment(None, ch, None, None)
            # space remains None

    def level_cleared(self):
        """Return True if no viruses remain in static grid."""
        for row in self.grid:
            for cell in row:
                if isinstance(cell, Virus):
                    return False
        return True

    def is_game_over(self):
        return self.game_over

    def handle_command(self, cmd):
        """Parse and execute a command string."""
        parts = shlex.split(cmd)
        if not parts:
            return
        op = parts[0]
        if op == 'F':
            if self.faller is None:
                # create new faller
                color1, color2 = parts[1], parts[2]
                mid = (self.cols // 2) - 1
                # if spawn collision, game over
                if any(self._cell_occupied(r, c)
                       for r, c, _ in Faller(color1, color2, mid).positions()):
                    self.game_over = True
                else:
                    self.faller = Faller(color1, color2, mid)
        elif op == 'V':
            # V row col color
            r, c, color = int(parts[1]), int(parts[2]), parts[3]
            if self.grid[r][c] is None:
                self.grid[r][c] = Virus(color)
        elif op in ('<', '>'):
            if self.faller:
                self._move_faller(-1 if op == '<' else 1)
        elif op == 'A':
            if self.faller:
                self._rotate_faller(clockwise=True)
        elif op == 'B':
            if self.faller:
                self._rotate_faller(clockwise=False)
        # Q handled in main loop

    def step(self):
        """Advance the game one time-step (blank input).
        Handles falling, landing, freezing, matching, and gravity."""
        if not self.faller:
            return
        # try to descend
        if self._can_descend():
            self.faller.row += 1
            self.faller.state = 'falling'
        else:
            if self.faller.state == 'falling':
                self.faller.state = 'landed'
            else:
                # freeze and integrate into static grid
                self._freeze_faller()
                self.faller = None
                # matching + gravity until stable
                while True:
                    matched = self._match_and_clear()
                    gravity = self._apply_gravity()
                    if not (matched or gravity):
                        break

    def _cell_occupied(self, r, c):
        """Return True if static cell at (r,c) is occupied or out of bounds."""
        return not (0 <= r < self.rows and 0 <= c < self.cols) or self.grid[r][c] is not None

    def _can_descend(self):
        """Return True if faller can move down one cell without collision."""
        for r, c, _ in self.faller.positions():
            if r + 1 >= self.rows or self.grid[r + 1][c] is not None:
                return False
        return True

    def _freeze_faller(self):
        """Convert landed faller segments into static CapsuleSegments."""
        cap_id = self.next_cap_id
        self.next_cap_id += 1
        pos = self.faller.positions()
        if self.faller.orientation == 'horizontal':
            # left segment at pos[0], right at pos[1]
            (r0, c0, col1), (r1, c1, col2) = pos
            self.grid[r0][c0] = CapsuleSegment(cap_id, col1, 'horizontal', 'left')
            self.grid[r1][c1] = CapsuleSegment(cap_id, col2, 'horizontal', 'right')
        else:
            # vertical: top pos[0], bottom pos[1]
            (r0, c0, col1), (r1, c1, col2) = pos
            self.grid[r0][c0] = CapsuleSegment(cap_id, col1, 'vertical', 'top')
            self.grid[r1][c1] = CapsuleSegment(cap_id, col2, 'vertical', 'bottom')

    def _match_and_clear(self):
        """Find and remove any groups of >=4 same-color cells horizontally or vertically.
        Returns True if any cells were cleared."""
        to_clear = set()
        # horizontal scans
        for r in range(self.rows):
            count = 1
            for c in range(1, self.cols):
                prev = self._cell_color(r, c - 1)
                curr = self._cell_color(r, c)
                if curr and prev == curr:
                    count += 1
                else:
                    if count >= 4:
                        for k in range(c - count, c): to_clear.add((r, k))
                    count = 1
            if count >= 4:
                for k in range(self.cols - count, self.cols): to_clear.add((r, k))
        # vertical scans
        for c in range(self.cols):
            count = 1
            for r in range(1, self.rows):
                prev = self._cell_color(r - 1, c)
                curr = self._cell_color(r, c)
                if curr and prev == curr:
                    count += 1
                else:
                    if count >= 4:
                        for k in range(r - count, r): to_clear.add((k, c))
                    count = 1
            if count >= 4:
                for k in range(self.rows - count, self.rows): to_clear.add((k, c))
        # clear them
        if not to_clear:
            return False
        for (r, c) in to_clear:
            self.grid[r][c] = None
        return True

    def _cell_color(self, r, c):
        """Helper: return color char at (r,c) or None."""
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return None
        cell = self.grid[r][c]
        if isinstance(cell, Virus) or isinstance(cell, CapsuleSegment):
            return cell.color
        return None

    def _apply_gravity(self):
        """Apply gravity to static capsules until no more moves possible.
        Returns True if any segment moved."""
        moved = False
        # process bottom-up
        for r in range(self.rows - 2, -1, -1):  # skip bottom row
            for c in range(self.cols):
                cell = self.grid[r][c]
                below = self.grid[r + 1][c]
                if cell and not isinstance(cell, Virus) and below is None:
                    # simple drop for any capsule segment
                    self.grid[r + 1][c] = cell
                    self.grid[r][c] = None
                    moved = True
        return moved

    def _move_faller(self, dc):
        """Attempt to move faller left/right by dc (-1 or +1)."""
        temp = Faller(self.faller.color1, self.faller.color2, self.faller.col)
        temp.orientation = self.faller.orientation
        temp.state = self.faller.state
        temp.row = self.faller.row
        temp.col = self.faller.col + dc
        # check bounds & collision
        if all(0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] is None
               for r, c, _ in temp.positions()):
            self.faller.col += dc
            # if was landed but now unsupported, resume falling
            if self.faller.state == 'landed' and self._can_descend():
                self.faller.state = 'falling'

    def _rotate_faller(self, clockwise=True):
        """Attempt to rotate faller, applying wall kick if needed."""
        temp = Faller(self.faller.color1, self.faller.color2, self.faller.col)
        temp.orientation = self.faller.orientation
        temp.state = self.faller.state
        temp.row = self.faller.row
        temp.rotate(clockwise)
        # try without kick
        if all(0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] is None
               for r, c, _ in temp.positions()):
            self.faller.orientation = temp.orientation
            return
        # if horizontal->vertical, try wall kick left
        if self.faller.orientation == 'horizontal':
            temp.col -= 1
            if all(0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] is None
                   for r, c, _ in temp.positions()):
                self.faller.orientation = temp.orientation
                self.faller.col -= 1
