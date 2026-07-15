#!/usr/bin/env python3

def write_maze(grid, entry, exit, solution, output_file):
    with open(output_file, 'w') as f:
        for line in grid:
            for cellule in line:
                f_hexa = format(cellule, 'X')
                f.write(f_hexa)
            f.write("\n")
        
        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit[0]},{exit[1]}\n")
        f.write(solution)


if __name__ == "__main__":
    from generator import MazeGenerator
    maze = MazeGenerator(5, 5, (0, 0), (4, 4), 42)
    maze.generate()
    write_maze(maze.get_grid(), maze.entry, maze.exit, maze.get_solution(), "test.txt")