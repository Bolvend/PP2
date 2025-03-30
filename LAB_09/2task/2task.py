import pygame
import random
import time

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
CELL = 30

# Font
font = pygame.font.SysFont("comicsansms", 20)

# FPS
clock = pygame.time.Clock()
FPS = 5

# Variables of score, level, snake's speed
food_cnt = 0
level_cnt = 1
snake_speed = 1

# Colors
colorGRAY = (169, 169, 169)
colorWHITE = (255, 255, 255)
colorRED = (255, 0, 0)
colorYELLOW = (255, 255, 0)
colorBLACK = (0, 0, 0)
colorGREEN = (0, 255, 0)
colorDOOL = (0, 0, 255)

# Draw Grid
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
        # Move the snake's body: each segment moves to the position of the previous one
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # Move the snake's head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # Handling border teleportation
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
        # Check for collisions with obstacles
        for obs in obstacles:
            if head.x == obs.x and head.y == obs.y:
                print("Game Over! Snake hit an obstacle.")
                pygame.quit()
                quit()
        # Check for collisions with food
        if head.x == food.pos.x and head.y == food.pos.y:
            print("Got food!")
            self.body.append(Point(head.x, head.y))
            # Update food count and level
            food_cnt += food.weight
            if food_cnt % 3 == 0:
                level_cnt += 1
                FPS += 0.5
            food.generate_random_pos(obstacles)

            

class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = random.randint(1, 3)  # Random weight for food (1 - low, 3 - high)
        self.time_to_live = random.randint(5, 10)  # Time for food to disappear (5 to 10 seconds)
        self.spawn_time = time.time()  # Time when food was spawned

    def draw(self):
        # Calculate color based on food weight
        if self.weight == 1:
            food_color = colorGREEN  # Light color for low-value food
        elif self.weight == 2:
            food_color = (0, 200, 0)  # Slightly darker green for medium-value food
        else:
            food_color = (0, 100, 0)  # Dark green for high-value food

        pygame.draw.rect(screen, food_color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, obstacles):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            # Check that the position is not occupied by the snake or obstacles
            if (not any(segment.x == self.pos.x and segment.y == self.pos.y for segment in snake.body) and
                not any(obs.x == self.pos.x and obs.y == self.pos.y for obs in obstacles)):
                break
        # Randomly generate a weight for the new food
        self.weight = random.randint(1, 3)
        # Reset food's spawn time
        self.spawn_time = time.time()

    def check_expiration(self):
        # Check if food has expired
        if time.time() - self.spawn_time > self.time_to_live:
            return True
        return False

FPS = 10
clock = pygame.time.Clock()

# Load obstacles from file (e.g., "map.txt")
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

    # Check if food expired and regenerate if necessary
    if food.check_expiration():
        food.generate_random_pos(obstacles)

    snake.draw()
    food.draw()

    # Level and score counters
    level = font.render("LEVEL " + str(level_cnt), True, colorBLACK)
    score = font.render("SCORE: " + str(food_cnt), True, colorBLACK)
    screen.blit(level, (5, 5))
    screen.blit(score, (5, 35))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
