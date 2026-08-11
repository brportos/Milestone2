"""Provide maze generation algorithms and pathfinding tools."""

import random
import sys


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

DIRECTIONS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}

WALL_BITS = {'N': NORTH, 'E': EAST, 'S': SOUTH, 'W': WEST}
OPPOSITE_DIR = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}
WALL = {'N': 1, 'E': 2, 'S': 4, 'W': 8}


class MazeGenerator:
    """Class responsible for generating grid mazes."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int,
        perfect: bool
    ) -> None:
        """Initialize maze parameters, random seed, and grid state."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        random.seed(seed)
        self.grid = [
            [15 for x in range(self.width)] for y in range(self.height)
            ]
        self.visited = [
            [False for x in range(self.width)] for y in range(self.height)
            ]

    def pattern_42(self) -> None:
        """Carve a solid 7x5 pattern '42' into the center of the maze grid.

        Raises:
            ValueError: If maze dimensions are smaller than 7x5.
        """
        PATTERN_42 = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]
        height_pattern = len(PATTERN_42)
        width_pattern = len(PATTERN_42[0])
        center_x = self.width // 2
        center_y = self.height // 2
        start_x = center_x - (width_pattern // 2)
        start_y = center_y - (height_pattern // 2)

        if self.width < 9 or self.height < 9:
            raise ValueError(
                "Error: Labyrinth width and height must be >= 9"
                )

        if self.width > 100 or self.height > 100:
            raise ValueError(
                "Error: Labyrinth width and height must be <= 100"
                )

        def _in_pattern_zone(x: int, y: int) -> bool:
            return (start_x <= x < start_x + width_pattern
                    and start_y <= y < start_y + height_pattern)

        entrance_x, entrance_y = self.entry
        exit_x, exit_y = self.exit

        if _in_pattern_zone(entrance_x, entrance_y):
            raise ValueError("Error: entrance is inside the pattern area")
        if _in_pattern_zone(exit_x, exit_y):
            raise ValueError("Error: exit is inside the pattern area")

        for y in range(height_pattern):
            for x in range(width_pattern):
                if PATTERN_42[y][x] == 1:
                    self.grid[start_y + y][start_x + x] = 15
                    self.visited[start_y + y][start_x + x] = True

    def depth_first_search(self) -> None:
        """Carve the maze paths using iterative Depth-First Search backtracker.

        Carves paths starting from the entry coordinate and optionally invokes
        the imperfect passage creator if `self.perfect` is False.
        """
        try:
            self.pattern_42()
            x, y = self.entry
            self.visited[y][x] = True
            stack = [(x, y)]

            while stack:
                cx, cy = stack[-1]
                unvisited = self.get_unvisited_voisin(cx, cy)

                if unvisited:
                    direction, nx, ny = random.choice(unvisited)
                    self.visited[ny][nx] = True
                    stack.append((nx, ny))
                    self.join_wall(cx, cy, nx, ny, direction)
                else:
                    stack.pop()

            if not self.perfect:
                self.imperfect_path()

        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)

    def get_unvisited_voisin(
        self,
        x: int,
        y: int
    ) -> list[tuple[str, int, int]]:
        """Find all unvisited adjacent neighbor cells within maze bounds.

        Args:
            x (int): Current cell horizontal index.
            y (int): Current cell vertical index.
        Returns:
            list[tuple[str, int, int]]:
            List of (direction, target_x, target_y) tuples.
        """
        voisins = []
        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and not self.visited[ny][nx]
            ):
                voisins.append((direction, nx, ny))
        return voisins

    def join_wall(
        self,
        x: int,
        y: int,
        nx: int,
        ny: int,
        direction: str
    ) -> None:
        """Remove adjacent walls between two neighboring cells.

        Args:
            x (int): Source cell X coordinate.
            y (int): Source cell Y coordinate.
            nx (int): Destination cell X coordinate.
            ny (int): Destination cell Y coordinate.
            direction (str): Direction of movement ('N', 'E', 'S', or 'W').
        """
        opp_direction = OPPOSITE_DIR[direction]
        wall = WALL_BITS[direction]
        opposite_wall = WALL_BITS[opp_direction]

        self.grid[y][x] &= ~wall
        self.grid[ny][nx] &= ~opposite_wall

    def get_grid(self) -> list[list[int]]:
        """Return the current state of the 2D maze grid.

        Returns:
            list[list[int]]: The integer matrix containing cell bitmasks.
        """
        return self.grid

    def is_inside_pattern_42(self, x: int, y: int) -> bool:
        """Check if a given coordinate lies inside the central Pattern 42.

        Args:
            x (int): Horizontal coordinate to test.
            y (int): Vertical coordinate to test.
        Returns:
            bool: True if coordinate overlaps pattern 42, False otherwise.
        """
        h_pat, w_pat = 5, 7
        start_x = (self.width // 2) - (w_pat // 2)
        start_y = (self.height // 2) - (h_pat // 2)
        return (
            start_x <= x < start_x + w_pat and start_y <= y < start_y + h_pat
        )

    def is_cell_open(self, x: int, y: int, direction: str) -> bool:
        """Return True if the wall in `direction`(x, y) is carved/open."""
        return (self.grid[y][x] & WALL_BITS[direction]) == 0

    def creates_3x3_open_area(self, target_x: int, target_y: int) -> bool:
        """Check if breaking a wall at (target_x, target_y).

        forms any 3x3 open block locally.
        """
        start_x_min = max(0, target_x - 2)
        start_x_max = min(self.width - 3, target_x)
        start_y_min = max(0, target_y - 2)
        start_y_max = min(self.height - 3, target_y)

        for y in range(start_y_min, start_y_max + 1):
            for x in range(start_x_min, start_x_max + 1):
                open_box = True
                for dy in range(3):
                    for dx in range(3):
                        cx, cy = x + dx, y + dy
                        if dx < 2 and not self.is_cell_open(cx, cy, 'E'):
                            open_box = False
                            break
                        if dy < 2 and not self.is_cell_open(cx, cy, 'S'):
                            open_box = False
                            break
                    if not open_box:
                        break

                if open_box:
                    return True
        return False

    def imperfect_path(self) -> None:
        """Randomly breaks walls to create cycles and multiple routes.

        Protects the inner Pattern 42 region and prevents 3x3 open areas.
        """
        attempts = (self.width * self.height) // 4
        for _ in range(attempts):
            rx = random.randint(0, self.width - 1)
            ry = random.randint(0, self.height - 1)

            if self.is_inside_pattern_42(rx, ry):
                continue

            d = random.choice(['N', 'E', 'S', 'W'])
            dx, dy = DIRECTIONS[d]
            nx, ny = rx + dx, ry + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.is_inside_pattern_42(nx, ny):
                    continue

                wall_bit = WALL_BITS[d]
                if not (self.grid[ry][rx] & wall_bit):
                    continue

                opp_bit = WALL_BITS[OPPOSITE_DIR[d]]
                self.grid[ry][rx] &= ~wall_bit
                self.grid[ny][nx] &= ~opp_bit

                if (
                    self.creates_3x3_open_area(rx, ry) or
                    self.creates_3x3_open_area(nx, ny)
                ):
                    self.grid[ry][rx] |= wall_bit
                    self.grid[ny][nx] |= opp_bit

    def breadth_first_search(self) -> str:
        """Find the shortest path from entry to exit using BFS traversal.

        Returns:
            str: Direction sequence string (e.g. "NNEESW") solving the maze.
        Raises:
            SystemExit: If pathfinding encounters an unexpected runtime error.
        """
        try:
            from collections import deque

            queue = deque([self.entry])
            visited: dict[
                tuple[int, int], tuple[int, int] | None
                ] = {self.entry: None}

            while queue:
                current = queue.popleft()
                if current == self.exit:
                    break

                cx, cy = current
                for d, (dx, dy) in DIRECTIONS.items():
                    nx, ny = cx + dx, cy + dy

                    if (
                        0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in visited
                    ):
                        if not (self.grid[cy][cx] & WALL[d]):
                            visited[(nx, ny)] = current
                            queue.append((nx, ny))

            path = []
            cell: tuple[int, int] | None = self.exit
            while cell is not None:
                path.append(cell)
                cell = visited.get(cell)
            path.reverse()

            offset_to_dir = {offset: d for d, offset in DIRECTIONS.items()}

            steps = []
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                steps.append(offset_to_dir[(x2 - x1, y2 - y1)])

            return "".join(steps)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
