import pygame
import random

CELL_SIZE = 30
WALL_COLOR = (139, 69, 19)
PATH_COLOR = (255, 228, 196)
GOAL_COLOR = (255, 0, 0)

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self.create_maze()
        self.squares = self.create_squares()
        self.start_pos, self.goal_pos = self.find_start_and_goal_positions()

    def create_maze(self):
        maze_width = self.width // CELL_SIZE
        maze_height = self.height // CELL_SIZE
        cells = [[False for _ in range(maze_width)] for _ in range(maze_height)]

        # Crear un laberinto de minotauro con caminos abiertos y cerrados
        for y in range(maze_height):
            for x in range(maze_width):
                if x == 0 or x == maze_width - 1 or y == 0 or y == maze_height - 1:
                    cells[y][x] = True
                else:
                    cells[y][x] = random.randint(0, 100) < 98

        # Asegurar un camino desde los puntos de inicio a la meta
        self.ensure_path(cells, 1, 1, maze_width - 2, maze_height - 2)

        return cells

    def ensure_path(self, cells, x1, y1, x2, y2):
        if x1 > x2 or y1 > y2:
            return

        # Crear un camino horizontal
        for x in range(x1, x2 + 2):
            cells[y1][x] = False
            cells[y2][x] = False

        # Crear un camino vertical
        for y in range(y1, y2 + 2):
            cells[y][x1] = False
            cells[y][x2] = False

        # Dividir recursivamente el laberinto
        self.ensure_path(cells, x1 + 2, y1 + 2, x2 - 2, y2 - 2)

    def create_squares(self):
        squares = []
        for _ in range(100):
            x = random.randint(1, self.width // CELL_SIZE - 2)
            y = random.randint(1, self.height // CELL_SIZE - 2)
            if not self.cells[y][x]:
                squares.append(((x*CELL_SIZE, 0), (x*CELL_SIZE, self.height), 0.5))
                squares.append(((0, y*CELL_SIZE), (self.width, y*CELL_SIZE), 0.5))
        return squares

    def find_start_and_goal_positions(self):
        start_pos = []
        maze_width = self.width // CELL_SIZE
        maze_height = self.height // CELL_SIZE

        # Encontrar las posiciones iniciales de los jugadores
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if not self.cells[y][x]:
                    if len(start_pos) < 2:
                        start_pos.append((x * CELL_SIZE, y * CELL_SIZE))

        # Establecer la posición de la meta en el centro del laberinto
        goal_x = (maze_width // 2) * CELL_SIZE
        goal_y = (maze_height // 2) * CELL_SIZE
        goal_pos = (goal_x, goal_y)

        return start_pos, goal_pos

    def draw(self, screen):
        screen.fill((0, 0, 0))

        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if self.cells[y][x]:
                    pygame.draw.rect(screen, WALL_COLOR, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, PATH_COLOR, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if self.goal_pos:
            pygame.draw.rect(screen, GOAL_COLOR, (self.goal_pos[0], self.goal_pos[1], CELL_SIZE, CELL_SIZE))

        new_squares = []
        for square in self.squares:
            if len(square) == 2 and len(square[0]) == 2 and len(square[1]) == 2:
                if square[0][0] == square[1][0]:
                    new_x0 = square[0][0]
                    new_y0 = square[0][1] + square[2]
                    new_x1 = square[1][0]
                    new_y1 = square[1][1] - square[2]
                else:
                    new_x0 = square[0][0] + square[2]
                    new_y0 = square[0][1]
                    new_x1 = square[1][0] - square[2]
                    new_y1 = square[1][1]
                new_squares.append(((new_x0, new_y0), (new_x1, new_y1)))
                pygame.draw.rect(screen, (255, 255, 255), (new_x0, new_y0, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (255, 255, 255), (new_x1, new_y1, CELL_SIZE, CELL_SIZE))
        self.squares = new_squares

        return self.start_pos, self.goal_pos