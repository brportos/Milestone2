#!/usr/bin/env python3
import random


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
    def __init__(self, width, height, entry, exit, seed):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        random.seed(seed)
        self.grid = [[15 for x in range(self.width)] for y in range(self.height)]
        self.visited = [[False for x in range(self.width)] for y in range(self.height)]

    def pattern_42(self):
        PATTERN_42 = [
            [1,0,0,1, 0, 1,1,1,1],
            [1,0,0,1, 0, 0,0,0,1],
            [1,1,1,1, 1, 1,1,1,1],
            [0,0,0,1, 0, 1,0,0,0],
            [0,0,0,1, 0, 1,1,1,1],
        ]
        height_pattern = len(PATTERN_42)
        width_pattern = len(PATTERN_42[0])
        center_x = self.width // 2
        center_y =self.height // 2
        start_x = center_x - (width_pattern // 2)
        start_y = center_y - (height_pattern // 2)
        if self.width < width_pattern or self.height < height_pattern:
            raise ValueError(f"Error: Labyrinth size is too small")
        for y in range(height_pattern):
            for x in range(width_pattern):
                if PATTERN_42[y][x] == 1:
                    self.grid[start_y + y][start_x + x] = 15
                    self.visited[start_y + y][start_x + x] = True
     
    def depth_first_search(self):
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

    def get_unvisited_voisin(self, x, y):
        voisins = []
        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny][nx]:
                voisins.append((direction, nx, ny))
        return voisins
    
    def join_wall(self, x, y, nx, ny, direction):
        opp_direction = OPPOSITE_DIR[direction]
        wall = WALL_BITS[direction]
        opposite_wall = WALL_BITS[opp_direction]

        self.grid[y][x] &= ~wall
        self.grid[ny][nx] &= ~opposite_wall

    def get_grid(self):
        return self.grid
    
    def breadth_first_search(self):
        from collections import deque

        queue = deque([self.entry])
        visited = {self.entry: None}
    
        while queue:
            current = queue.popleft()
            if current == self.exit:
                break
            
            cx, cy = current
            for d, (dx, dy) in DIRECTIONS.items():
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    if not (self.grid[cy][cx] & WALL[d]):
                        visited[(nx, ny)] = current
                        queue.append((nx, ny))

        path = []
        cell = self.exit
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
