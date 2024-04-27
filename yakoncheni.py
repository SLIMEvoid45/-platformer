import pygame
import sys
import json

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.jump_power = -15
        self.move_speed = 5

    def update(self, platforms):
        self.vel_y += 1
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

        # Коллизии с платформами
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for plat in collisions:
            if self.vel_y > 0:
                self.rect.bottom = plat.rect.top
                self.vel_y = 0
            elif self.vel_y < 0:
                self.rect.top = plat.rect.bottom
                self.vel_y = 0

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.move_speed
        elif keys[pygame.K_RIGHT]:
            self.vel_x = self.move_speed
        else:
            self.vel_x = 0

        if keys[pygame.K_SPACE] and self.rect.bottom >= HEIGHT:
            self.vel_y = self.jump_power
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Функция для создания уровня из файла JSON
def load_level(file_name):
    with open(file_name, 'r') as f:
        level_data = json.load(f)
    platforms = pygame.sprite.Group()
    for plat in level_data['platforms']:
        p = Platform(*plat)
        platforms.add(p)
    return platforms

# Функция для основного игрового цикла
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    player = Player(100, HEIGHT - 100)
    platforms = load_level('level1.json')  # Загрузка уровня из JSON
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update()
        collisions = pygame.sprite.spritecollide(player, platforms, False)
        for plat in collisions:
            if player.vel_y > 0:
                player.rect.bottom = plat.rect.top
                player.vel_y = 0
            elif player.vel_y < 0:
                player.rect.top = plat.rect.bottom
                player.vel_y = 0

        # Отрисовка
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
if __name__ == "__main__":
    main()
