import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки игры
WIDTH, HEIGHT = 300, 600  # Размеры окна
CELL_SIZE = 30  # Размер ячейки
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE  # Количество колонок и строк
SCORE = 0

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Определяем фигуры тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # Линия
    [[1, 1, 0], [0, 1, 1]],  # Z-образная
    [[0, 1, 1], [1, 1, 0]],  # Обратная Z-образная
    [[1, 1], [1, 1]],  # Квадрат
    [[1, 1, 1], [0, 1, 0]],  # Т-образная
    [[1, 1, 1], [1, 0, 0]],  # L-образная
    [[1, 1, 1], [0, 0, 1]]   # Обратная L-образная
]

# Цвета фигур
SHAPE_COLORS = [CYAN, RED, GREEN, YELLOW, PURPLE, ORANGE, BLUE]

# Класс фигуры
class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, win):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(win, self.color, (self.x * CELL_SIZE + j * CELL_SIZE, self.y * CELL_SIZE + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def collision(self, grid, dx=0, dy=0):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x]):
                        return True
        return False

# Функция создания пустого игрового поля
def create_grid():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Функция добавления фигуры на поле
def place_shape(grid, shape):
    for i, row in enumerate(shape.shape):
        for j, cell in enumerate(row):
            if cell:
                grid[shape.y + i][shape.x + j] = shape.color

# Функция проверки и удаления заполненных линий
def clear_lines(grid):
    global SCORE
    cleared_lines = 0
    for i in range(len(grid)):
        if 0 not in grid[i]:
            del grid[i]
            grid.insert(0, [0 for _ in range(COLS)])
            cleared_lines += 1
    SCORE += cleared_lines ** 2 * 100

# Основной игровой цикл
def game_loop():
    global SCORE
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

    grid = create_grid()
    current_shape = Tetromino(random.choice(SHAPES))
    next_shape = Tetromino(random.choice(SHAPES))

    clock = pygame.time.Clock()
    fall_time = 0
    speed = 500  # Скорость падения фигур
    running = True

    while running:
        grid_copy = [row[:] for row in grid]  # Копия для отображения падения фигуры
        win.fill(BLACK)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not current_shape.collision(grid, dx=-1):
                    current_shape.x -= 1
                elif event.key == pygame.K_RIGHT and not current_shape.collision(grid, dx=1):
                    current_shape.x += 1
                elif event.key == pygame.K_DOWN and not current_shape.collision(grid, dy=1):
                    current_shape.y += 1
                elif event.key == pygame.K_UP:
                    current_shape.rotate()
                    if current_shape.collision(grid):
                        current_shape.rotate()
                        current_shape.rotate()
                        current_shape.rotate()

        # Движение фигуры вниз по таймеру
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time > speed:
            if not current_shape.collision(grid, dy=1):
                current_shape.y += 1
            else:
                place_shape(grid, current_shape)
                current_shape = next_shape
                next_shape = Tetromino(random.choice(SHAPES))
                if current_shape.collision(grid):
                    print(f"Game Over! Your score: {SCORE}")
                    running = False
            fall_time = 0

        # Проверка заполненных линий
        clear_lines(grid)

        # Отрисовка сетки и текущей фигуры
        current_shape.draw(win)
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j]:
                    pygame.draw.rect(win, grid[i][j], (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {SCORE}", True, WHITE)
        win.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()

game_loop()
