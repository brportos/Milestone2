import sys
from maze import MazeGenerator
from maze import write_maze
from maze import parse_config 
import os

from mlx import Mlx 
tile_size = 30
class Renderer:
    def __init__(self, width: int = 500, height: int = 400) -> None:
        self.width: int = width
        self.height: int = height

        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        self.win = self.mlx.mlx_new_window(self.mlx_ptr, width, height, "A_maze_ing")

        self.img = self.mlx.mlx_new_image(self.mlx_ptr, width, height)
        
        self.data, self.bpp, self.sl, _ = self.mlx.mlx_get_data_addr(self.img)

    def put_pixel(self, x: int, y: int, color: int) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            off = y * self.sl + x * (self.bpp // 8)
            self.data[off:off + 4] = color.to_bytes(4, 'little')

    def flush(self, param=None) -> int:
        """Pushes the image buffer to the window."""
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, self.img, 0, 0)
        return 0

    def draw_rect(self, x_start: int, y_start: int, width: int, height: int, color: int) -> None:
        """Fills a solid rectangle with a color (perfect for tiles/paths)"""
        for y in range(y_start, y_start + height):
            for x in range(x_start, x_start + width):
                self.put_pixel(x, y, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        """Draws a straight horizontal or vertical line (perfect for walls)"""
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.put_pixel(x1, y, color)
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.put_pixel(x, y1, color)
    
    def handle_keypress(self, key: int, param) -> int:
        """Handles keypress events. Esc closes the window."""
        if key in (65307, 53, 52):
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win)
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def draw_maze(self, maze, path_str: str) -> None:
        grid = maze.get_grid()
        
        BG_COLOR = 0x00000000   
        WALL_COLOR = 0xFFFFFFFF
        SOLUTION_COLOR = 0xFF000000
        ENTRY_COLOR = 0xFF00FF00
        EXIT_COLOR = 0xFFFF0000

        for y in range(maze.height):
            for x in range(maze.width):
                px = x * tile_size
                py = y * tile_size
                cell_value = grid[y][x]

                self.draw_rect(px, py, tile_size, tile_size, BG_COLOR)

                if grid[y][x] & 1 != 0:
                    self.draw_line(px, py, px + tile_size, py, WALL_COLOR)
                if grid[y][x] & 2 != 0:
                    self.draw_line(px + tile_size, py, px + tile_size, py + tile_size, WALL_COLOR)
                if grid[y][x] & 4 != 0:
                    self.draw_line(px, py + tile_size, px + tile_size, py + tile_size, WALL_COLOR)
                if grid[y][x] & 8 != 0:
                    self.draw_line(px, py, px, py + tile_size, WALL_COLOR)
                if grid[y][x] == 1:
                    self.draw_line(px, py, px, py + tile_size, SOLUTION_COLOR)

        self.draw_rect(maze.entry[0] * tile_size + 4, maze.entry[1] * tile_size + 4, tile_size - 8, tile_size - 8, ENTRY_COLOR)
        self.draw_rect(maze.exit[0] * tile_size + 4, maze.exit[1] * tile_size + 4, tile_size - 8, tile_size - 8, EXIT_COLOR)

        curr_x, curr_y = maze.entry
        for move in path_str:
            self.draw_rect(curr_x * tile_size + 7, curr_y * tile_size + 7, 6, 6, SOLUTION_COLOR)
            if move == 'N': curr_y -= 1
            elif move == 'S': curr_y += 1
            elif move == 'E': curr_x += 1
            elif move == 'W': curr_x -= 1
        self.draw_rect(curr_x * tile_size + 7, curr_y * tile_size + 7, 6, 6, SOLUTION_COLOR)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    config_file = sys.argv[1]
    config = parse_config(config_file)

    maze = MazeGenerator(20, 15, (0, 0), (19, 14), 42)
    maze.depth_first_search()
    path_str = maze.breadth_first_search()

    renderer = Renderer(maze.width * tile_size, maze.height * tile_size)
    renderer.draw_maze(maze, path_str)

    renderer.mlx.mlx_key_hook(renderer.win, renderer.handle_keypress, None)
    
    renderer.mlx.mlx_loop_hook(renderer.mlx_ptr, renderer.flush, None)
    
    renderer.mlx.mlx_loop(renderer.mlx_ptr)