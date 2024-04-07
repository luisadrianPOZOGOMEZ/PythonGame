import pygame
from network import Network

class Player():
    segment_width = segment_height = 10

    def __init__(self, startx, starty, player_id, color=(0,255,0)):
        self.segments = [(startx, starty)]
        self.velocity = 10
        self.color = color
        self.player_id = player_id

    def draw(self, g):
        for segment in self.segments:
            pygame.draw.rect(g, self.color, (segment[0], segment[1], self.segment_width, self.segment_height))
            font = pygame.font.Font(None, 20)
            text = font.render("P " + str(self.player_id), True, (94, 51, 255))
            g.blit(text, (segment[0] + 2, segment[1] + 2))

    def move(self, dirn):
        x, y = self.segments[0]

        if dirn == 0:
            x += self.velocity
        elif dirn == 1:
            x -= self.velocity
        elif dirn == 2:
            y -= self.velocity
        else:
            y += self.velocity

        self.segments = [(x, y)] + self.segments[:-1]

    def grow(self):
        x, y = self.segments[-1]
        self.segments.append((x, y))

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50, 1)
        self.player2 = Player(100,100, 2)
        self.canvas = Canvas(self.width, self.height, "Testing...")

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
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.segments[0][0] >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.segments[0][1] >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.segments[0][1] <= self.height - self.player.velocity:
                    self.player.move(3)

            self.player2.segments[0] = self.parse_data(self.send_data())

            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

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

class Canvas:

    def __init__(self, w, h, name="None"):
        pygame.font.init()  # Inicializa la fuente aquí
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
        self.screen.fill((255,255,255))