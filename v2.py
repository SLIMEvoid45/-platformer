import pygame
import random
import json
pygame.init()
WIDTH, HEIGHT = 1200, 800
TILE_SIZE = 15
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
WATER_BLUE = (0, 191, 255)
EMPTY = 0
GRASS = 1
STONE = 2
WATER = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("lolgcghjkljhxfghj")
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 40
player_speed = 5
world = []
for row in range(HEIGHT // TILE_SIZE):
    new_row = []
    for col in range(WIDTH // TILE_SIZE):

            new_row.append(STONE)

    world.append(new_row)
selected_block = GRASS
grass_img = pygame.image.load("sp3.png").convert_alpha()
stone_img = pygame.image.load("sp2.png").convert_alpha()
water_img = pygame.image.load("sp1.png").convert_alpha()
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
                pass
                
def save_world():
    with open("world.json", "w") as file:
        json.dump(world, file)
    
def load_world():
    global world
    with open("world.json", "r") as file:
        world = json.load(file)
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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            click_x = mouse_pos[0] // TILE_SIZE
            click_y = mouse_pos[1] // TILE_SIZE  
            if 0 <= click_x < len(world[0]) and 0 <= click_y < len(world):  
                if event.button == 1: 
                    if world[click_y][click_x] != EMPTY:
                        world[click_y][click_x] = EMPTY
                elif event.button == 3: 
                    if world[click_y][click_x] == EMPTY:
                        world[click_y][click_x] = selected_block

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: 
                if player_pos[1] >= 0:
                    player_pos[1] -= player_speed
                    
            elif event.key == pygame.K_DOWN:  
                if player_pos[1] <= HEIGHT - player_size:
                    player_pos[1] += player_speed
            elif event.key == pygame.K_LEFT:  
                if player_pos[0] >= 0:
                    player_pos[0] -= player_speed
            elif event.key == pygame.K_RIGHT: 
                if player_pos[0] <= WIDTH - player_size:
                    player_pos[0] += player_speed
            elif event.key == pygame.K_s:  
                save_world()
            elif event.key == pygame.K_l: 
                load_world()
            elif event.key == pygame.K_1:  
                selected_block = GRASS
            elif event.key == pygame.K_2: 
                selected_block = STONE
            elif event.key == pygame.K_3:  
                selected_block = WATER


    screen.fill(WHITE)
    draw_world()
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.display.flip()
    pygame.time.Clock().tick(30)
pygame.quit()

