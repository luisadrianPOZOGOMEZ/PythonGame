import pygame
from network import Network
from maze import Maze, WALL_COLOR, PATH_COLOR, GOAL_COLOR, CELL_SIZE

class Player(object):
    def __init__(self, startx, starty, player_id, color=(0,255,0)):
        self.segments = [(startx, starty)]
        self.player_id = player_id
        self.color = color
        self.segment_width = 20
        self.segment_height = 20
        self.velocity = 10

    def move(self, direction, maze):
        x, y = self.segments[0]
        new_x, new_y = x, y

        if direction == 0:  # right
            new_x = x + self.velocity
        elif direction == 1:  # left
            new_x = x - self.velocity
        elif direction == 2:  # up
            new_y = y - self.velocity
        elif direction == 3:  # down
            new_y = y + self.velocity

        # Comprobar si la nueva posición está dentro de los límites del laberinto y no hay pared
        if 0 <= new_x < maze.width and 0 <= new_y < maze.height and not maze.cells[new_y // CELL_SIZE][new_x // CELL_SIZE]:
            self.segments.insert(0, (new_x, new_y))
            self.segments.pop()

    def draw(self, g):
        for segment in self.segments:
            pygame.draw.rect(g, self.color, (segment[0], segment[1], self.segment_width, self.segment_height))
            font = pygame.font.Font(None, 20)
            text = font.render("P " + str(self.player_id), True, (94, 51, 255))
            g.blit(text, (segment[0] + 2, segment[1] + 2))

class Game:
    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.maze = Maze(self.width, self.height)
        start_pos, self.goal_pos = self.maze.start_pos, self.maze.goal_pos
        self.player = Player(start_pos[0][0], start_pos[0][1], 1)
        self.player2 = Player(start_pos[1][0], start_pos[1][1], 2)
        self.canvas = Canvas(self.width, self.height, "Minotaur Maze")
        self.player_won = False

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.player.segments[0][0] <= self.width - self.player.velocity:
                    self.player.move(0, self.maze)
                    if abs(self.player.segments[0][0] - self.goal_pos[0]) < CELL_SIZE and abs(self.player.segments[0][1] - self.goal_pos[1]) < CELL_SIZE:
                        print("Jugador 1 ha llegado al objetivo!")
                        self.player_won = True
                        run = False

            if keys[pygame.K_LEFT]:
                if self.player.segments[0][0] >= self.player.velocity:
                    self.player.move(1, self.maze)
                    if abs(self.player.segments[0][0] - self.goal_pos[0]) < CELL_SIZE and abs(self.player.segments[0][1] - self.goal_pos[1]) < CELL_SIZE:
                        print("Jugador 1 ha llegado al objetivo!")
                        self.player_won = True
                        run = False

            if keys[pygame.K_UP]:
                if self.player.segments[0][1] >= self.player.velocity:
                    self.player.move(2, self.maze)
                    if abs(self.player.segments[0][0] - self.goal_pos[0]) < CELL_SIZE and abs(self.player.segments[0][1] - self.goal_pos[1]) < CELL_SIZE:
                        print("Jugador 1 ha llegado al objetivo!")
                        self.player_won = True
                        run = False

            if keys[pygame.K_DOWN]:
                if self.player.segments[0][1] <= self.height - self.player.velocity:
                    self.player.move(3, self.maze)
                    if abs(self.player.segments[0][0] - self.goal_pos[0]) < CELL_SIZE and abs(self.player.segments[0][1] - self.goal_pos[1]) < CELL_SIZE:
                        print("Jugador 1 ha llegado al objetivo!")
                        self.player_won = True
                        run = False

            self.player2.segments[0] = self.parse_data(self.send_data())
            if abs(self.player2.segments[0][0] - self.goal_pos[0]) < CELL_SIZE and abs(self.player2.segments[0][1] - self.goal_pos[1]) < CELL_SIZE:
                print("Jugador 2 ha llegado al objetivo!")
                self.player_won = True
                run = False

            self.canvas.draw_background()
            self.maze.draw(self.canvas.get_canvas())
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())

            # Draw the goal
            if self.goal_pos:
                pygame.draw.rect(self.canvas.get_canvas(), GOAL_COLOR,
                                (self.goal_pos[0], self.goal_pos[1], CELL_SIZE, CELL_SIZE))

            self.canvas.update()

        if self.player_won:
            self.show_winner_message()
            self.canvas.update()
            pygame.time.delay(2000)
            self.restart_game()  # Reiniciar el juego

        pygame.quit()

    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player.segments[0][0]) + "," + str(self.player.segments[0][1])
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

    def show_winner_message(self):
        self.canvas.draw_text("¡Felicidades, has ganado!", 50, self.width // 2 - 200, self.height // 2 - 50)
        self.canvas.update()
        pygame.time.delay(2000)

    def restart_game(self):
        self.player_won = False
        start_pos, self.goal_pos = self.maze.start_pos, self.maze.goal_pos
        self.player.segments = [start_pos[0]]
        self.player2.segments = [start_pos[1]]


class Canvas:
    def __init__(self, w, h, name="None"):
        pygame.font.init()
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))
        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0, 0, 0))