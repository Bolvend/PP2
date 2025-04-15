import pygame
import psycopg2
import json
import random
import time

pygame.init()

# Константы
WIDTH = 600
HEIGHT = 600
CELL = 30
GRID_WIDTH = WIDTH // CELL
GRID_HEIGHT = HEIGHT // CELL
FPS = 10

# Цвета
colorWHITE = (255, 255, 255)
colorGRAY = (169, 169, 169)
colorRED = (255, 0, 0)
colorYELLOW = (255, 255, 0)
colorBLACK = (0, 0, 0)
colorGREEN = (0, 255, 0)
colorDOOL = (0, 0, 255)

# Шрифт
font = pygame.font.SysFont("comicsansms", 20)

# Подключение к базе данных
conn_params = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": "12345678",
    "host": "localhost",
    "port": "5432"
}

def connect():
    try:
        conn = psycopg2.connect(**conn_params)
        print("Подключение к базе данных успешно")
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

# Создание таблиц
def create_tables():
    conn = connect()
    if conn is None:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_name VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_score (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                level INTEGER NOT NULL,
                score INTEGER NOT NULL,
                saved_state JSONB NOT NULL,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Table creation error: {e}")
    finally:
        cur.close()
        conn.close()

# Регистрация или поиск пользователя
def get_or_register_user(user_name):
    conn = connect()
    if conn is None:
        print("Не удалось подключиться к базе данных")
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE user_name = %s", (user_name,))
        result = cur.fetchone()
        if result:
            print(f"Пользователь {user_name} найден, ID: {result[0]}")
            return result[0]
        print(f"Пользователь {user_name} не найден, регистрируем...")
        cur.execute("INSERT INTO users (user_name) VALUES (%s) RETURNING id", (user_name,))
        user_id = cur.fetchone()[0]
        conn.commit()
        print(f"Пользователь {user_name} зарегистрирован, ID: {user_id}")
        return user_id
    except Exception as e:
        print(f"Ошибка регистрации: {e}")
        return None
    finally:
        cur.close()
        conn.close()

# Загрузка текущего уровня пользователя
def load_user_level(user_id):
    conn = connect()
    if conn is None:
        return 1
    try:
        cur = conn.cursor()
        cur.execute("SELECT level FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
        result = cur.fetchone()
        return result[0] if result else 1
    except Exception as e:
        print(f"Level load error: {e}")
        return 1
    finally:
        cur.close()
        conn.close()

# Сохранение состояния игры
def save_game(user_id, level, score, snake, food):
    conn = connect()
    if conn is None:
        return
    try:
        cur = conn.cursor()
        state = {
            "snake": [(p.x, p.y) for p in snake.body],
            "snake_direction": (snake.dx, snake.dy),
            "food": {
                "x": food.pos.x,
                "y": food.pos.y,
                "weight": food.weight,
                "time_to_live": food.time_to_live,
                "spawn_time": food.spawn_time
            }
        }
        state_json = json.dumps(state)
        cur.execute(
            "INSERT INTO user_score (user_id, level, score, saved_state) VALUES (%s, %s, %s, %s)",
            (user_id, level, score, state_json)
        )
        conn.commit()
        print("Игра сохранена")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
    finally:
        cur.close()
        conn.close()

# Загрузка последнего сохраненного состояния
def load_game(user_id):
    conn = connect()
    if conn is None:
        return None
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT level, score, saved_state FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1",
            (user_id,)
        )
        result = cur.fetchone()
        if result:
            level, score, state_json = result
            state = json.loads(state_json)
            return level, score, state
        return None
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None
    finally:
        cur.close()
        conn.close()

# Отрисовка шахматного фона
def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(screen, colors[(i + j) % 2], (j * CELL, i * CELL, CELL, CELL))

# Отрисовка препятствий
def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, colorDOOL, (obs.x * CELL, obs.y * CELL, CELL, CELL))

# Загрузка карты уровня
def load_map(level):
    filename = f"level{level}.txt"
    obstacles = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for y, line in enumerate(lines):
                line = line.strip()
                for x, char in enumerate(line):
                    if char == '#':
                        obstacles.append(Point(x, y))
    except FileNotFoundError:
        print(f"Файл {filename} не найден, создаем пустую карту")
    return obstacles

# Класс Point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

# Класс Snake
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def reset(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy
        if self.body[0].x > GRID_WIDTH - 1:
            self.body[0].x = 0
        if self.body[0].x < 0:
            self.body[0].x = GRID_WIDTH - 1
        if self.body[0].y > GRID_HEIGHT - 1:
            self.body[0].y = 0
        if self.body[0].y < 0:
            self.body[0].y = GRID_HEIGHT - 1

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food, obstacles):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        for obs in obstacles:
            if head.x == obs.x and head.y == obs.y:
                return True
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            return "food"
        return False

# Класс Food
class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = random.randint(1, 3)
        self.time_to_live = random.randint(5, 10)
        self.spawn_time = time.time()

    def draw(self):
        if self.weight == 1:
            food_color = colorGREEN
        elif self.weight == 2:
            food_color = (0, 200, 0)
        else:
            food_color = (0, 100, 0)
        pygame.draw.rect(screen, food_color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake, obstacles):
        while True:
            self.pos.x = random.randint(0, GRID_WIDTH - 1)
            self.pos.y = random.randint(0, GRID_HEIGHT - 1)
            if (not any(segment.x == self.pos.x and segment.y == self.pos.y for segment in snake.body) and
                not any(obs.x == self.pos.x and obs.y == self.pos.y for obs in obstacles)):
                print(f"Новая еда сгенерирована на позиции ({self.pos.x}, {self.pos.y})")
                break
            else:
                print(f"Позиция ({self.pos.x}, {self.pos.y}) занята, генерируем новую")
        self.weight = random.randint(1, 3)
        self.time_to_live = random.randint(5, 10)
        self.spawn_time = time.time()

    def check_expiration(self):
        if time.time() - self.spawn_time > self.time_to_live:
            return True
        return False

# Инициализация игры
create_tables()
username = input("Введите имя пользователя: ")
user_id = get_or_register_user(username)
if user_id is None:
    print("Не удалось зарегистрировать или найти пользователя. Выход.")
    pygame.quit()
    exit()

current_level = load_user_level(user_id)
print(f"Текущий уровень: {current_level}")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

snake = Snake()
food = Food()
score = 0

# Загрузка сохраненного состояния
saved_state = load_game(user_id)
obstacles = load_map(current_level)
if saved_state:
    level, score, state = saved_state
    snake.body = [Point(x, y) for x, y in state["snake"]]
    snake.dx, snake.dy = state["snake_direction"]
    food.pos = Point(state["food"]["x"], state["food"]["y"])
    food.weight = state["food"]["weight"]
    food.time_to_live = state["food"]["time_to_live"]
    food.spawn_time = state["food"]["spawn_time"]
    current_level = level
    if (any(segment.x == food.pos.x and segment.y == food.pos.y for segment in snake.body) or
        any(obs.x == food.pos.x and obs.y == food.pos.y for obs in obstacles)):
        print("Еда перекрывается с змейкой или препятствием, генерируем новую")
        food.generate_random_pos(snake, obstacles)
else:
    food.generate_random_pos(snake, obstacles)

# Основной игровой цикл
running = True
paused = False
pause_until = 0  # Время, до которого игра должна быть на паузе
food_eaten = 0
FOOD_TO_NEXT_LEVEL = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(user_id, current_level, score, snake, food)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    save_game(user_id, current_level, score, snake, food)
                    print("Игра приостановлена и сохранена")
                else:
                    print("Игра возобновлена")
            if not paused and time.time() >= pause_until:
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx = 1
                    snake.dy = 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx = -1
                    snake.dy = 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx = 0
                    snake.dy = 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx = 0
                    snake.dy = -1

    # Проверяем, не на паузе ли игра (по клавише P или из-за перехода на уровень)
    is_paused = paused or (time.time() < pause_until)

    if not is_paused:
        snake.move()
        collision = snake.check_collision(food, obstacles)
        if collision == "food":
            score += food.weight
            food_eaten += 1
            food.generate_random_pos(snake, obstacles)
            if food_eaten >= FOOD_TO_NEXT_LEVEL:
                current_level += 1
                if current_level > 3:
                    current_level = 1
                food_eaten = 0
                snake.reset()
                score = 0
                obstacles = load_map(current_level)
                print(f"Переход на уровень {current_level}")
                pause_until = time.time() + 3  # Пауза на 3 секунды при переходе на уровень
        elif collision:
            print("Game Over!")
            save_game(user_id, current_level, score, snake, food)
            running = False

        if food.check_expiration():
            food.generate_random_pos(snake, obstacles)

    # Отрисовка
    draw_grid_chess()
    draw_obstacles(obstacles)
    snake.draw()
    food.draw()

    # Счетчики уровня и очков
    level_text = font.render("LEVEL " + str(current_level), True, colorBLACK)
    score_text = font.render("SCORE: " + str(score), True, colorBLACK)
    screen.blit(level_text, (5, 5))
    screen.blit(score_text, (5, 35))

    # Отображение состояния паузы
    if is_paused:
        pause_text = font.render("PAUSED", True, colorBLACK)
        screen.blit(pause_text, (WIDTH // 2 - 40, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()