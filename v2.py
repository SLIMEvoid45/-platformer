import pygame
import random
import json

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 15
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
WATER_BLUE = (0, 191, 255)

# Типы блоков
EMPTY = 0
GRASS = 1
STONE = 2
WATER = 3

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Minecraft")

# Создание игрока
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 40
player_speed = 5

# Создание мира
world = []
for row in range(HEIGHT // TILE_SIZE):
    new_row = []
    for col in range(WIDTH // TILE_SIZE):
        rand = random.random()
        if rand < 0.1:
            new_row.append(STONE)
        elif rand < 0.2:
            new_row.append(WATER)
        elif rand < 0.3:
            new_row.append(GRASS)
        else:
            new_row.append(EMPTY)
    world.append(new_row)

# Выбранный тип блока
selected_block = GRASS
# Загрузка изображений спрайтов блоков
grass_img = pygame.image.load("sp3.png").convert_alpha()
stone_img = pygame.image.load("sp2.png").convert_alpha()
water_img = pygame.image.load("sp1.png").convert_alpha()

# Функция отрисовки мира
def draw_world():
    for row in range(len(world)):
        for col in range(len(world[row])):
            if world[row][col] == GRASS:
                screen.blit(grass_img, (col * TILE_SIZE, row * TILE_SIZE))
            elif world[row][col] == STONE:
                screen.blit(stone_img, (col * TILE_SIZE, row * TILE_SIZE))
            elif world[row][col] == WATER:
                screen.blit(water_img, (col * TILE_SIZE, row * TILE_SIZE))
            else:
                # Если блок пустой, не отрисовываем ничего
                pass


# Функция сохранения мира в файл JSON
def save_world():
    with open("world.json", "w") as file:
        json.dump(world, file)

# Функция загрузки мира из файла JSON
def load_world():
    global world
    with open("world.json", "r") as file:
        world = json.load(file)

# Функция проверки коллизий игрока с миром
def check_collision(rect, dx, dy):
    for y in range(rect.top // TILE_SIZE, (rect.bottom + TILE_SIZE - 1) // TILE_SIZE):
        for x in range(rect.left // TILE_SIZE, (rect.right + TILE_SIZE - 1) // TILE_SIZE):
            if 0 <= x < len(world[0]) and 0 <= y < len(world):
                if world[y][x] in [GRASS, STONE, WATER]:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(tile_rect):
                        if dx > 0:
                            dx = tile_rect.left - rect.right
                        if dx < 0:
                            dx = tile_rect.right - rect.left
                        if dy > 0:
                            dy = tile_rect.top - rect.bottom
                        if dy < 0:
                            dy = tile_rect.bottom - rect.top
    return dx, dy

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            click_x = mouse_pos[0] // TILE_SIZE
            click_y = mouse_pos[1] // TILE_SIZE
            # Проверяем, находится ли клик мыши в пределах допустимых индексов мира
            if 0 <= click_x < len(world[0]) and 0 <= click_y < len(world):
                if event.button == 1:  # Левая кнопка мыши (разрушение блока)
                    if world[click_y][click_x] != EMPTY:
                        world[click_y][click_x] = EMPTY
                elif event.button == 3:  # Правая кнопка мыши (установка блока)
                    if world[click_y][click_x] == EMPTY:
                        world[click_y][click_x] = selected_block
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Нажатие стрелки вверх (прыжок)
                if player_pos[1] >= 0:
                    player_pos[1] -= player_speed
            elif event.key == pygame.K_DOWN:  # Нажатие стрелки вниз (движение вниз)
                if player_pos[1] <= HEIGHT - player_size:
                    player_pos[1] += player_speed
            elif event.key == pygame.K_LEFT:  # Нажатие стрелки влево (движение влево)
                if player_pos[0] >= 0:
                    player_pos[0] -= player_speed
            elif event.key == pygame.K_RIGHT:  # Нажатие стрелки вправо (движение вправо)
                if player_pos[0] <= WIDTH - player_size:
                    player_pos[0] += player_speed
            elif event.key == pygame.K_s:  # Нажатие клавиши "S" (сохранение мира)
                save_world()
            elif event.key == pygame.K_l:  # Нажатие клавиши "L" (загрузка мира)
                load_world()
            elif event.key == pygame.K_1:  # Нажатие клавиши "1" (выбор блока GRASS)
                selected_block = GRASS
            elif event.key == pygame.K_2:  # Нажатие клавиши "2" (выбор блока STONE)
                selected_block = STONE
            elif event.key == pygame.K_3:  
                selected_block = WATER

    # Отрисовка
    screen.fill(WHITE)
    draw_world()
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.display.flip()

    # Ограничение частоты кадров
    pygame.time.Clock().tick(30)

# Выход из игры
pygame.quit()
