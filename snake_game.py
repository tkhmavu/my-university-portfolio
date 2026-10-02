import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Определение цветов (RGB)
BACKGROUND = (30, 30, 46)
GRID_COLOR = (40, 40, 60)
SNAKE_HEAD = (116, 252, 116)
SNAKE_BODY = (80, 220, 80)
FOOD_COLOR = (255, 95, 95)
TEXT_COLOR = (205, 214, 244)
PANEL_COLOR = (49, 50, 68)

# Параметры игрового поля
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT + 60  # Место для верхней панели

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Красивая Змейка (Snake)')
clock = pygame.time.Clock()

# Шрифты
font_small = pygame.font.SysFont('Arial', 20, bold=True)
font_large = pygame.font.SysFont('Arial', 40, bold=True)

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 1),
            (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 2)
        ]
        self.direction = (0, -1)
        self.next_direction = (0, -1)
        self.score = 0
        self.grow = False

    def update(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Проверка столкновения со стеной или с собой
        if (new_head in self.body or
            not (0 <= new_head[0] < GRID_WIDTH) or
            not (0 <= new_head[1] < GRID_HEIGHT)):
            return False

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def draw(self, surface):
        for index, block in enumerate(self.body):
            x = block[0] * CELL_SIZE
            y = block[1] * CELL_SIZE + 60
            rect = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            
            # Разные цвета для головы и тела
            color = SNAKE_HEAD if index == 0 else SNAKE_BODY
            pygame.draw.rect(surface, color, rect, border_radius=8)

class Food:
    def __init__(self, snake_body):
        self.position = self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, surface):
        x = self.position[0] * CELL_SIZE + CELL_SIZE // 2
        y = self.position[1] * CELL_SIZE + 60 + CELL_SIZE // 2
        pygame.draw.circle(surface, FOOD_COLOR, (x, y), CELL_SIZE // 2 - 4)

def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(60, WINDOW_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

def main():
    snake = Snake()
    food = Food(snake.body)
    game_over = False

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        snake.reset()
                        food = Food(snake.body)
                        game_over = False
                else:
                    if event.key == pygame.K_w and snake.direction != (0, 1):
                        snake.next_direction = (0, -1)
                    elif event.key == pygame.K_s and snake.direction != (0, -1):
                        snake.next_direction = (0, 1)
                    elif event.key == pygame.K_a and snake.direction != (1, 0):
                        snake.next_direction = (-1, 0)
                    elif event.key == pygame.K_d and snake.direction != (-1, 0):
                        snake.next_direction = (1, 0)

        # Игровая логика
        if not game_over:
            if not snake.update():
                game_over = True

            # Поедание еды
            if snake.body[0] == food.position:
                snake.grow = True
                snake.score += 1
                food = Food(snake.body)

        # Очистка экрана
        screen.fill(BACKGROUND)

        # Отрисовка верхней панели
        pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WINDOW_WIDTH, 60))
        score_text = font_small.render(f"СЧЕТ: {snake.score}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 20))

        # Отрисовка элементов игры
        draw_grid(screen)
        food.draw(screen)
        snake.draw(screen)

        # Если игра окончена
        if game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((30, 30, 46, 200))
            screen.blit(overlay, (0, 0))

            game_over_text = font_large.render("ИГРА ОКОНЧЕНА", True, FOOD_COLOR)
            restart_text = font_small.render("Нажмите 'R' для перезапуска", True, TEXT_COLOR)
            
            screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 40))
            screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(10)  # Скорость змейки (FPS)

if __name__ == '__main__':
    main()
