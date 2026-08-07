"""Main entry point for the A-Maze-ing generator and visualizer."""
import sys
from mazegen import MazeGenerator
from writer import write_maze
from config import parse_config
import os


try:
    from mlx import Mlx
except Exception as e:
    print(f"\nERROR: {e}")
    print("To make it works, run: make install")
    print("And then: source env/bin/activate")
    print("Finally: make\n")
    sys.exit(1)

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

MARGIN_BOTTOM = 40
WALL_COLORS = [
    0xFFFFFFFF,
    0xFF00FF00,
    0xFFDC143C,
    0xFFFFFF00,
    0xFFFF00FF,
    0xFF00FFFF,
    0xFFFFDAB9,
    0xFFE6E6FA,
]


class Renderer:
    """Manages maze graphics and MiniLibX input.

    Attributes:
        mlx (Mlx): MiniLibX library instance wrapper.
        mlx_ptr (Any): Pointer to the MLX environment instance.
        cell_size (int): Pixel dimension for each individual maze cell.
        width (int): Total window width in pixels.
        height (int): Total window height in pixels including margin.
        maze_width (int): Column count of the maze.
        maze_height (int): Row count of the maze.
        win (Any): MLX window pointer.
        img (Any): MLX image buffer pointer.
        data (Any): Byte array representing the image pixel framebuffer.
        bpp (int): Bits per pixel in the framebuffer.
        sl (int): Scanline stride (bytes per row) of the image buffer.
        grid (list[list[int]] | None): 2D integer matrix of maze walls.
        entry (tuple[int, int] | None): Entry coordinate (x, y).
        exit (tuple[int, int] | None): Exit coordinate (x, y).
        chemin (str | list[tuple[int, int]] | None):
        Path solution sequence or coordinates.
        show_path (bool): Toggle indicator for displaying solution dots.
        perfect (bool): True if maze has a single unique path, False otherwise.
        seed (int): Current seed used for maze generation.
        color_index (int): Index selector for the wall color palette.
        wall_color (int): Active wall color hex value.
    """

    def __init__(
        self,
        maze_width: int,
        maze_height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool
    ) -> None:
        """Initialize MLX window and event hooks."""
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        """cell size calculation"""
        _, screen_w, screen_h = self.mlx.mlx_get_screen_size(self.mlx_ptr)
        cell_w = screen_w // maze_width
        cell_h = (screen_h - MARGIN_BOTTOM - 100) // maze_height
        self.cell_size = min(cell_w, cell_h, 30)
        self.cell_size = max(self.cell_size, 5)

        """Window size calculation"""
        self.width = maze_width * self.cell_size
        self.height = maze_height * self.cell_size + MARGIN_BOTTOM
        self.maze_width = maze_width
        self.maze_height = maze_height

        """create window et image with good size"""
        self.win = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.width,
            self.height,
            "A_MAZE_ING"
            )
        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            self.width,
            self.height
            )
        self.data, self.bpp, self.sl, _ = self.mlx.mlx_get_data_addr(self.img)

        """hooks"""
        self.mlx.mlx_key_hook(self.win, self.key_hook, None)
        self.mlx.mlx_hook(self.win, 33, 0, self.destroy, None)

        """given labyrinthe"""
        self.grid: list[list[int]] | None = None
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.chemin: str | list[tuple[int, int]] | None = None
        self.show_path = False
        self.perfect = perfect
        self.seed = 0
        self.color_index = 0
        self.wall_color = 0xFFFFFFFF

    def put_pixel(self, x: int, y: int, color: int) -> None:
        """Write a single color pixel into the image buffer(x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            off: int = y * self.sl + x * (self.bpp // 8)
            self.data[off:off+4] = color.to_bytes(4, 'little')

    def flush(self) -> None:
        """Pushe the memory image buffer to the active MLX window."""
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win,
            self.img,
            0,
            0
            )

    def draw_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: int
    ) -> None:
        """Fill a rectangular region in the image buffer with a solid color.

        Args:
            x (int): Starting horizontal coordinate of top-left corner.
            y (int): Starting vertical coordinate of top-left corner.
            width (int): Rectangle width in pixels.
            height (int): Rectangle height in pixels.
            color (int): 32-bit ARGB color value.
        """
        for dy in range(height):
            for dx in range(width):
                self.put_pixel(x + dx, y + dy, color)

    def clear(self) -> None:
        """Clear the entire image framebuffer data to black bytes."""
        size = self.height * self.sl
        self.data[:size] = bytes(size)

    def key_hook(self, keycode: int, params: None) -> int:
        """Procedure keyboard input events triggered within the window.

        Args:
            keycode (int): System keycode identifier of the pressed key.
            params (Any): Unused hook parameter passed by MLX.
        Returns:
            int: Standard hook exit code (0).
        """
        if keycode == 0:
            return 0
        if keycode == 65307:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        elif keycode == 97:
            self.seed += 1

            new_maze = MazeGenerator(
                self.maze_width,
                self.maze_height,
                self.entry,
                self.exit,
                self.seed,
                self.perfect
                )

            self.redraw()
            new_maze.depth_first_search()
            if not new_maze.perfect:
                new_maze.imperfect_path()
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

    def destroy(self, params: None) -> None:
        """Destroy the process upon clicking the window close button.

        Args:
            params (Any): Unused event parameter.
        Returns:
            int: Standard exit status code.
        """
        os._exit(0)
        return 0

    def draw_maze(
        self,
        grid: list[list[int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        width: int,
        height: int,
        chemin: str | list[tuple[int, int]] | None,
        show_path: bool
    ) -> None:
        """Render walls, start/exit points, pattern 42, and path into buffer.

        Args:
            grid (list[list[int]] | None): Matrix containing wall bitmasks.
            entry (tuple[int, int] | None): Entry cell coordinates.
            exit (tuple[int, int] | None): Exit cell coordinates.
            width (int): Total column count.
            height (int): Total row count.
            chemin (str | list[tuple[int, int]] | None): Solution path.
            show_path (bool): True to draw solution path dots, False otherwise.
        """
        WALL_SIZE = 1
        CELL_SIZE = self.cell_size
        WALL_COLOR = self.wall_color
        ENTRY_COLOR = 0xFF00FF00
        EXIT_COLOR = 0xFFFF0000
        PATH_COLOR = 0xFF00FFFF
        COLOR_42 = 0xFF4B0082

        path: list[tuple[int, int]] = []
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

        elif isinstance(chemin, list):
            path = chemin

        for y in range(height):
            for x in range(width):
                pixel_x = x * CELL_SIZE
                pixel_y = y * CELL_SIZE

                if (x, y) == entry:
                    self.draw_rect(
                        pixel_x,
                        pixel_y,
                        CELL_SIZE,
                        CELL_SIZE,
                        ENTRY_COLOR
                        )

                if (x, y) == exit:
                    self.draw_rect(
                        pixel_x,
                        pixel_y,
                        CELL_SIZE,
                        CELL_SIZE,
                        EXIT_COLOR
                        )
                if show_path and (x, y) in path:
                    dot_size = 6
                    cx = pixel_x + CELL_SIZE // 2 - dot_size // 2
                    cy = pixel_y + CELL_SIZE // 2 - dot_size // 2
                    self.draw_rect(cx, cy, dot_size, dot_size, PATH_COLOR)
                if grid[y][x] == 15:
                    self.draw_rect(
                        pixel_x,
                        pixel_y,
                        CELL_SIZE,
                        CELL_SIZE,
                        COLOR_42
                        )
                if grid[y][x] & NORTH != 0:
                    self.draw_rect(
                        pixel_x,
                        pixel_y,
                        CELL_SIZE,
                        WALL_SIZE,
                        WALL_COLOR
                        )
                if grid[y][x] & SOUTH != 0:
                    self.draw_rect(
                        pixel_x,
                        pixel_y + CELL_SIZE - WALL_SIZE,
                        CELL_SIZE,
                        WALL_SIZE,
                        WALL_COLOR
                        )
                if grid[y][x] & WEST != 0:
                    self.draw_rect(
                        pixel_x,
                        pixel_y,
                        WALL_SIZE,
                        CELL_SIZE,
                        WALL_COLOR
                        )
                if grid[y][x] & EAST != 0:
                    self.draw_rect(
                        pixel_x + CELL_SIZE - WALL_SIZE,
                        pixel_y,
                        WALL_SIZE,
                        CELL_SIZE,
                        WALL_COLOR
                        )

        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win,
            10,
            self.height - 25,
            0xFFFFFFFF,
            "a:regen  w:show/hide path  d:Change_color  esc:quit"
            )

    def redraw(self) -> None:
        """Clear the window image buffer and triggers full scene re-render."""
        if self.grid is None or self.entry is None or self.exit is None:
            return
        self.clear()
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win)
        self.draw_maze(
            self.grid, self.entry, self.exit,
            self.maze_width, self.maze_height,
            self.chemin, self.show_path
            )
        self.flush()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <config_file>")
        sys.exit(1)

    config = parse_config(sys.argv[1])

    maze = MazeGenerator(
        config["WIDTH"],
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
        config["SEED"],
        config["PERFECT"]
    )
    maze.depth_first_search()
    chemin = maze.breadth_first_search()

    write_maze(
        maze.get_grid(),
        maze.entry,
        maze.exit,
        chemin,
        config["OUTPUT_FILE"]
    )

    render = Renderer(
        config["WIDTH"],
        config["HEIGHT"],
        maze.entry,
        maze.exit,
        config["PERFECT"]
        )
    render.grid = maze.get_grid()
    render.entry = maze.entry
    render.exit = maze.exit
    render.chemin = chemin
    render.seed = config["SEED"]

    render.redraw()

    render.mlx.mlx_loop(render.mlx_ptr)
