#!/usr/bin/env python3
import random

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

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
        start_x = center_x - width_pattern // 2
        start_y = center_y - height_pattern // 2
        if start_x < 0 or start_y < 0:
            raise ValueError("Error: small labyrinth")
        if start_x + width_pattern > self.width:
            raise ValueError("Error: width small")
        if start_y + height_pattern > self.height:
            raise ValueError("Error: heigth small")
        for y in range(height_pattern):
            for x in range(width_pattern):
                if PATTERN_42[y][x] == 1:
                    self.grid[start_y + y][start_x + x] = 15
                    self.visited[start_y + y][start_x + x] = True
     
    def depth_first_search(self):
        self.pattern_42()
        x = self.entry[0]
        y = self.entry[1]
        self.visited[y][x] = True
        stack = [(x, y)]
        while stack:
            last = stack[-1]
            x = last[0]
            y = last[1]
            unvisited_voisin = self.get_unvisited_voisin(x, y)
            if unvisited_voisin:
                voisin = random.choice(unvisited_voisin)
                next_x = voisin[0]
                next_y = voisin[1]
                direction = voisin[2]
                self.visited[next_y][next_x] = True
                stack.append((next_x, next_y))
                self.join_wall(x, y, next_x, next_y, direction)
            else:
                stack.pop()

    def get_unvisited_voisin(self, x, y):
        voisins = []
        if y - 1 >= 0 and self.visited[y - 1][x] == False:
            voisins.append((x, y - 1, NORTH))
        if x + 1 < self.width and self.visited[y][x + 1] == False:
            voisins.append((x + 1, y, EAST))
        if y + 1 < self.height and self.visited[y + 1][x] == False:
            voisins.append((x, y + 1, SOUTH))
        if x - 1 >= 0 and self.visited[y][x - 1] == False:
            voisins.append((x - 1, y, WEST))
        return voisins
    
    def join_wall(self, x, y, nx, ny, direction):
        if direction == NORTH:
            self.grid[y][x] &= ~NORTH
            self.grid[ny][nx] &= ~SOUTH
        elif direction == EAST:
            self.grid[y][x] &= ~EAST
            self.grid[ny][nx] &= ~WEST
        elif direction == SOUTH:
            self.grid[y][x] &= ~SOUTH
            self.grid[ny][nx] &= ~NORTH
        elif direction == WEST:
            self.grid[y][x] &= ~WEST
            self.grid[ny][nx] &= ~EAST

    def get_grid(self):
        return self.grid
    
    def breadth_first_search(self):
        from collections import deque

        file = deque()
        file.append(self.entry)
        parent = {self.entry: None}
        while file:
            current = file.popleft()
            if current == self.exit:
                break
            x = current[0]
            y = current[1]
            for voisin in self.get_accessible_voisin(x, y):
                if voisin not in parent:
                    parent[voisin] = current
                    file.append(voisin)
        chemin = []
        cellule = self.exit
        while cellule != None:
            chemin.append(cellule)
            cellule = parent[cellule]
        chemin.reverse()

        convert_chemin = ""
        for i in range(len(chemin) - 1):
            cellule1 = chemin[i]
            cellule2 = chemin[i + 1]
            x1 = cellule1[0]
            y1 = cellule1[1]
            x2 = cellule2[0]
            y2 = cellule2[1]
            if x2 > x1:
                convert_chemin += 'E'
            elif x1 > x2:
                convert_chemin += 'W'
            elif y1 > y2:
                convert_chemin += 'N'
            elif y2 > y1:
                convert_chemin += 'S'
        return convert_chemin

    def get_accessible_voisin(self, x, y):
        voisins = []
        if y - 1 >= 0 and self.grid[y][x] & NORTH == 0:
            voisins.append((x, y - 1))
        if x + 1 < self.width and self.grid[y][x] & EAST == 0:
            voisins.append((x + 1, y))
        if y + 1 < self.height and self.grid[y][x] & SOUTH == 0:
            voisins.append((x, y + 1))
        if x - 1 >= 0 and self.grid[y][x] & WEST == 0:
            voisins.append((x - 1, y))
        return voisins
