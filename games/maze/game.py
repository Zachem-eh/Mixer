import sys
from random import randint

from utils import const
from utils.tools import load_image, resize_screen, lvl_passed
import pygame


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


def load_level(filename):
    global level_map
    filename = "data/maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def init():
    global tile_images, player_image, tile_width, tile_height, all_sprites, tiles_group, player_group, player, level_x, level_y, \
        FPS, WIDTH, HEIGHT, lightning_group, clock
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png'),
        'lightning': load_image('lightning2.png')
    }
    player_image = load_image('capybara.png')

    WIDTH, HEIGHT = size = 1000, 1000
    const.screen = resize_screen(*size)

    FPS = 50
    clock = pygame.time.Clock()

    lightning_group = pygame.sprite.Group()

    tile_width = tile_height = 50

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    level = randint(1, 3)
    level_map = load_level('map' + str(level) + '.txt')
    player, level_x, level_y = generate_level(level_map)


def handler_event(event):
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
                return lvl_passed()


def post_loop_step():
    const.screen.fill('white')
    tiles_group.draw(const.screen)
    lightning_group.draw(const.screen)
    player_group.draw(const.screen)
    pygame.display.flip()
    clock.tick(FPS)
