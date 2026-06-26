import pygame
import random

# Инициализация
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Dino:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.width = 40
        self.height = 60
        self.is_jumping = False
        self.jump_count = 10

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

    def jump(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count > 0 else -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10


class Obstacle:
    def __init__(self, speed):
        self.width = random.randint(30, 50)
        self.height = random.randint(40, 80)
        self.x = SCREEN_WIDTH
        self.y = 360 - self.height
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x -= self.speed


def reset_game():
    return Dino(), [], 0, 5  # Возвращаем нового дино, пустой список, счет и начальную скорость


dino = Dino()
obstacles = []
score = 0
game_speed = 5
running = True
game_over = False

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    dino.is_jumping = True
                else:
                    dino, obstacles, score, game_speed = reset_game()
                    game_over = False

    if not game_over:
        dino.jump()
        score += 1
        # Увеличение скорости каждые 500 очков
        if score % 500 == 0:
            game_speed += 0.5

        # Генерация препятствий
        if len(obstacles) == 0 or obstacles[-1].x < SCREEN_WIDTH - 300:
            obstacles.append(Obstacle(game_speed))

        for obs in obstacles[:]:
            obs.move()
            if obs.x < -obs.width:
                obstacles.remove(obs)

            # Столкновение
            if (dino.x < obs.x + obs.width and dino.x + dino.width > obs.x and
                    dino.y + dino.height > obs.y):
                game_over = True

        dino.draw(screen)
        for obs in obstacles:
            obs.draw(screen)
    else:
        # Экран проигрыша
        font = pygame.font.SysFont(None, 55)
        text = font.render("GAME OVER! Press Space", True, BLACK)
        screen.blit(text, (150, 150))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()