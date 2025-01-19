from random import randint

import pygame
import sys
import os

pygame.init()

FPS = 50
WIDTH, HEIGHT = size = 1000, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'lightning': load_image('lightning2.png')
}
player_image = load_image('capybara.png')

tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
lightning_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Lightning(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(lightning_group, all_sprites)
        self.image = tile_images['lightning']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = pos_x, pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Lightning(x, y)
    return new_player, x, y


level = randint(1, 3)
level_map = load_level('map' + str(level) + '.txt')
player, level_x, level_y = generate_level(level_map)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            x, y = player.pos
            if event.key == pygame.K_UP and level_map[y - 1][x] != '#':
                player.pos = x, y - 1
                player.rect.y -= tile_height
            if event.key == pygame.K_DOWN and level_map[y + 1][x] != '#':
                player.pos = x, y + 1
                player.rect.y += tile_height
            if event.key == pygame.K_LEFT and level_map[y][x - 1] != '#':
                player.pos = x - 1, y
                player.rect.x -= tile_width
            if event.key == pygame.K_RIGHT and level_map[y][x + 1] != '#':
                player.pos = x + 1, y
                player.rect.x += tile_width

            for lightning in lightning_group:
                if player.pos == lightning.pos:
                    lightning.kill()

    screen.fill('white')
    tiles_group.draw(screen)
    lightning_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()