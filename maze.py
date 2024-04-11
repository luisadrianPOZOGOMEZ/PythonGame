import pygame
import random

# Configuración del laberinto
CELL_SIZE = 30
WALL_COLOR = (139, 69, 19)  # Color marrón oscuro para las paredes
PATH_COLOR = (255, 228, 196)  # Color beige claro para los caminos
GOAL_COLOR = (255, 0, 0)  # Color rojo para la meta

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self.create_maze()
        self.squares = self.create_squares()
        self.start_pos = self.find_start_positions()
        self.goal_pos = self.find_goal_position()

    def create_maze(self):
        maze_width = self.width // CELL_SIZE
        maze_height = self.height // CELL_SIZE

        cells = [[False for _ in range(maze_width)] for _ in range(maze_height)]

        # Crear un laberinto de minotauro con caminos abiertos y cerrados
        for y in range(maze_height):
            for x in range(maze_width):
                if x == 0 or x == maze_width - 1 or y == 0 or y == maze_height - 1 or (x % 2 == 0 and y % 2 == 0):
                    cells[y][x] = True
                elif random.randint(0, 100) < 30:
                    cells[y][x] = True

        return cells

    def create_squares(self):
        squares = []
        for _ in range(100):
            x = random.randint(1, self.width // CELL_SIZE - 2)
            y = random.randint(1, self.height // CELL_SIZE - 2)
            if not self.cells[y][x]:
                squares.append(((x*CELL_SIZE, 0), (x*CELL_SIZE, self.height), 0.5))
                squares.append(((0, y*CELL_SIZE), (self.width, y*CELL_SIZE), 0.5))
        return squares

    def find_start_positions(self):
        start_pos = []
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if not self.cells[y][x]:
                    start_pos.append((x*CELL_SIZE, y*CELL_SIZE))
                    if len(start_pos) == 2:
                        return start_pos
        return start_pos

    def find_goal_position(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if not self.cells[y][x]:
                    if random.randint(0, 100) < 10:
                        return (x*CELL_SIZE, y*CELL_SIZE)
        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Limpiar la pantalla con color negro
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if self.cells[y][x]:
                    pygame.draw.rect(screen, WALL_COLOR, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, PATH_COLOR, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Dibujar la meta
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