"""Provide utilities to export generated mazes and solutions to disk."""

import sys


def write_maze(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    path: str,
    output_file: str
) -> None:
    """Write the generated maze grid, coordinates, and path to a file.

    Formats the 2D matrix into hexadecimal representations and appends the
    entry, exit, and solution path strings at the bottom of the output.
    Args:
        grid (list[list[int]]):
        2D array representing wall bitmasks for each cell.
        entry (tuple[int, int]): Starting coordinates (x, y) of the maze.
        exit (tuple[int, int]): Target coordinates (x, y) of the maze.
        path (str):
        Sequence of direction steps (e.g., "NNEESW") solving the maze.
        output_file (str): Destination file path to write the formatted maze.
    Raises:
        SystemExit: Exits the process if writing to disk fails.
    """
    try:
        with open(output_file, 'w') as f:
            for line in grid:
                for cellule in line:
                    f_hexa = format(cellule, 'X')
                    f.write(f_hexa)
                f.write("\n")

            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(path)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
