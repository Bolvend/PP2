import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
CELL = 30
#Font
font = pygame.font.SysFont("comicsansms", 20)

# FPS
clock = pygame.time.Clock()
FPS = 5

# Variables of score, level, snake's speed
food_cnt = 0
level_cnt = 1
snake_speed = 1

# Определение цветов
colorGRAY = (169, 169, 169)
colorWHITE = (255, 255, 255)
colorRED = (255, 0, 0)
colorYELLOW = (255, 255, 0)
colorBLACK = (0, 0, 0)
colorGREEN = (0, 255, 0)
colorDOOL = (0, 0, 255)

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]

    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, colorDOOL, (obs.x * CELL, obs.y * CELL, CELL, CELL))

def load_map(filename):
    obstacles = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for y, line in enumerate(lines):
            line = line.strip()
            for x, char in enumerate(line):
                if char == '#':
                    obstacles.append(Point(x, y))
    return obstacles

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        # Передвигаем тело змейки: каждый сегмент переходит в позицию предыдущего
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # Передвигаем голову змейки
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # Обработка выхода за границы экрана (телепортация)
        if self.body[0].x > WIDTH // CELL - 1:
            self.body[0].x = 0
        if self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1
        if self.body[0].y > HEIGHT // CELL - 1:
            self.body[0].y = 0
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food, obstacles):
        global food_cnt, level_cnt, FPS

        head = self.body[0]
        # Проверка столкновения с препятствиями
        for obs in obstacles:
            if head.x == obs.x and head.y == obs.y:
                print("Game Over! Snake hit an obstacle.")
                pygame.quit()
                quit()
        # Проверка столкновения с едой
        if head.x == food.pos.x and head.y == food.pos.y:
            print("Got food!")
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos(obstacles)

            # Увеличение счётчика пищи и уровня
            food_cnt += 1
            if food_cnt % 3 == 0:
                level_cnt += 1
                # Увеличение скорости игры (FPS)
                FPS += 0.5

class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, obstacles):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            # Проверка, чтобы новая позиция не совпадала с телом змейки и препятствиями
            if (not any(segment.x == self.pos.x and segment.y == self.pos.y for segment in snake.body) and
                not any(obs.x == self.pos.x and obs.y == self.pos.y for obs in obstacles)):
                break

FPS = 10
clock = pygame.time.Clock()

# Загрузка препятствий из файла (например, "map.txt")
obstacles = load_map("map.txt")
food = Food()
snake = Snake()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1

    screen.fill(colorBLACK)

    draw_grid_chess()
    draw_obstacles(obstacles)

    snake.move()
    snake.check_collision(food, obstacles)

    snake.draw()
    food.draw()
     #Level and score counters
    level = font.render("LEVEL " + str(level_cnt), True, colorBLACK)
    score = font.render("SCORE: " + str(food_cnt), True, colorBLACK)
    food.draw()
    screen.blit(level, (5, 5))
    screen.blit(score, (5, 35))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
