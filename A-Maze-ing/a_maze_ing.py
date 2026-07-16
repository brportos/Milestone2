import sys
from generator import MazeGenerator
from writer import write_maze
from config import parse_config 
import os
from mlx import Mlx 
tile_size = 30


from mlx import Mlx
import os

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
CELL_SIZE = 30
MARGIN_BOTTOM = 40
WALL_COLORS = [
    0xFFFFFFFF,   # blanc
    0xFF00FF00,   # vert
    0xFFFFFF00,   # jaune
    0xFFFF00FF,   # magenta
    0xFF00FFFF,   # cyan
]

class Renderer:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win = self.mlx.mlx_new_window(self.mlx_ptr, width, height, "A-Maze-ing")
        """creation d'image"""
        self.img = self.mlx.mlx_new_image(self.mlx_ptr, width, height)
        self.data: memoryview
        self.bpp: int
        self.sl: int
        self.data, self.bpp, self.sl, _ = \
            self.mlx.mlx_get_data_addr(self.img)
        """les hooks"""
        self.mlx.mlx_key_hook(self.win, self.key_hook, None)
        self.mlx.mlx_hook(self.win, 33, 0, self.destroy, None)

        """les donner du labyrinth"""
        self.grid = None
        self.entry = None
        self.exit = None
        self.maze_width = None
        self.maze_height = None
        self.chemin = None
        self.show_path = False
        self.seed = 0
        
        """couleur des mur"""
        self.color_index = 0
        self.wall_color = 0xFFFFFFFF
    def put_pixel(self, x: int, y: int, color: int) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            off: int = y * self.sl + x * (self.bpp // 8)
            self.data[off:off+4] = color.to_bytes(4, 'little')
        
    def flush(self) -> None:
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, self.img, 0, 0)
    
    def draw_rect(self, x, y, width, height, color):
        for dy in range(height):
            for dx in range(width):
                self.put_pixel(x + dx, y + dy, color)

    def redraw(self):
        self.clear()
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win)
        self.draw_maze(self.grid, self.entry, self.exit,
                      self.maze_width, self.maze_height,
                      self.chemin, self.show_path)
        self.flush()

    def clear(self):
        size = self.height * self.sl
        self.data[:size] = bytes(size)
    
    def key_hook(self, keycode, params):
        if keycode == 0:
            return 0
        if keycode == 65307:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        elif keycode == 97:
            self.seed += 1
            from generator import MazeGenerator

            new_maze = MazeGenerator(self.maze_width, self.maze_height,
                                     self.entry, self.exit, self.seed)
            
            self.redraw()
            new_maze.depth_first_search()
            self.grid = new_maze.get_grid()
            self.chemin = new_maze.breadth_first_search()
            self.redraw()
        elif keycode == 119:
            self.show_path = not self.show_path
            self.redraw()
        
        elif keycode == 100:
            self.color_index = (self.color_index + 1) % len(WALL_COLORS)
            self.wall_color = WALL_COLORS[self.color_index]
            self.redraw()
        return 0

    def destroy(self, params):
        os._exit(0)
        return 0
    def draw_maze(self, grid, entry, exit, width, height, chemin, show_path):
        WALL_SIZE = 2
        WALL_COLOR  = self.wall_color
        ENTRY_COLOR = 0xFF00FF00
        EXIT_COLOR  = 0xFFFF0000 
        PATH_COLOR  = 0xFF00FFFF
        COLOR_42    = 0xFF005500

        if isinstance(chemin, str):
            path = [entry]
            curr_x, curr_y = entry

            for direction in chemin:
                if direction == 'N':
                    curr_y -= 1
                elif direction == 'S':
                    curr_y += 1
                elif direction == 'E':
                    curr_x += 1
                elif direction == 'W':
                    curr_x -= 1
                path.append((curr_x, curr_y))
            chemin = path
        
        for y in range(height):
            for x in range(width):
                pixel_x = x * CELL_SIZE
                pixel_y = y * CELL_SIZE

                if (x,y) == entry:
                    self.draw_rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE, ENTRY_COLOR)
                    
                if (x, y) == exit:
                    self.draw_rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE, EXIT_COLOR)
                if show_path and (x, y) in chemin:
                    dot_size = 6
                    cx = pixel_x + CELL_SIZE // 2 - dot_size // 2
                    cy = pixel_y + CELL_SIZE // 2 - dot_size // 2
                    self.draw_rect(cx, cy, dot_size, dot_size, PATH_COLOR)
                if grid[y][x] == 15:
                    self.draw_rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE, COLOR_42)
                if grid[y][x] & NORTH != 0:
                    self.draw_rect(pixel_x, pixel_y, CELL_SIZE, WALL_SIZE, WALL_COLOR)
                if grid[y][x] & SOUTH != 0:
                    self.draw_rect(pixel_x, pixel_y + CELL_SIZE - WALL_SIZE, CELL_SIZE, WALL_SIZE, WALL_COLOR)
                if grid[y][x] & WEST != 0:
                    self.draw_rect(pixel_x, pixel_y, WALL_SIZE, CELL_SIZE, WALL_COLOR)
                if grid[y][x] & EAST != 0:
                    self.draw_rect(pixel_x + CELL_SIZE - WALL_SIZE, pixel_y, WALL_SIZE, CELL_SIZE, WALL_COLOR)
        
        self.mlx.mlx_string_put(
        self.mlx_ptr, self.win,
        10,
        self.height - 25,
        0xFFFFFFFF,
        "a:regen  w:show/hide path  d:Change_color  esc:quit"
        )

        return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("error, The argument must be")
        sys.exit()
    colors_index=0
    show_path = False
    config = parse_config(sys.argv[1])
    maze = MazeGenerator(config["WIDTH"],config["HEIGHT"],config["ENTRY"], config["EXIT"],config["SEED"])
    maze.depth_first_search()
    chemin = maze.breadth_first_search()
    write_maze(maze.get_grid(), maze.entry, maze.exit, chemin, config["OUTPUT_FILE"])
    render = Renderer(config["WIDTH"] * CELL_SIZE, config["HEIGHT"] * CELL_SIZE + MARGIN_BOTTOM)
    """stockage des valeur de la labyrinthe"""
    render.grid = maze.get_grid()
    render.entry = maze.entry
    render.exit = maze.exit
    render.maze_width = config["WIDTH"]
    render.maze_height = config["HEIGHT"]
    render.chemin = chemin
    render.seed = config["SEED"]
    render.draw_maze(maze.get_grid(), maze.entry, maze.exit,
                        config["WIDTH"], config["HEIGHT"], chemin, show_path)
    render.flush()
    render.mlx.mlx_loop(render.mlx_ptr)

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         sys.exit(1)

#     config_file = sys.argv[1]
#     config = parse_config(config_file)
#     show_path = False

#     maze = MazeGenerator(config["WIDTH"], config["HEIGHT"], (0, 0), (config["WIDTH"] - 1, config["HEIGHT"] - 1), 42)
#     maze.depth_first_search()
#     path_str = maze.breadth_first_search()
#     write_maze(maze.get_grid(), maze.entry, maze.exit, path_str, config["OUTPUT_FILE"])

#     renderer = Renderer(maze.width * tile_size, maze.height * tile_size)
#     renderer.draw_maze(maze, config["ENTRY"], config["EXIT"], config["WIDTH"], config["HEIGHT"], path_str, show_path)

#     renderer.mlx.mlx_key_hook(renderer.win, renderer.handle_keypress, None)
    
#     renderer.mlx.mlx_loop_hook(renderer.mlx_ptr, renderer.flush, None)
    
#     renderer.mlx.mlx_loop(renderer.mlx_ptr)