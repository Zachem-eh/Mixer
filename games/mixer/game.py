import random

import sys

import pygame

from utils import const
from utils.tools import load_image, resize_screen


class Board(pygame.sprite.Sprite):
    def __init__(self, group, _width, _height):
        super().__init__(group)
        self.add(board_group)
        self.width = _width
        self.height = _height
        self.cell_size = const.screen.get_width() // (self.width + 10)
        self.image = pygame.Surface((self.width * self.cell_size, self.width * self.cell_size), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((const.screen.get_width() - self.cell_size * self.width) / 2,
                                   (const.screen.get_height() - self.cell_size * self.height) / 1.8)
        self.board = [[0] * _width for _ in range(_height)]
        gen_x, gen_y = random.randrange(self.width), random.randrange(self.height)
        self.board[gen_y][gen_x] = Generator(all_sprites, self, gen_x, gen_y)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(self.image, 'black', (self.cell_size * x,
                                                       self.cell_size * y, self.cell_size, self.cell_size), 1)

    def update(self, *args):
        pass

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (x < self.rect.x or x > self.rect.x + self.width * self.cell_size) or \
                (y < self.rect.y or y > self.rect.y + self.height * self.cell_size):
            return None
        return (x - self.rect.x) // self.cell_size, (y - self.rect.y) // self.cell_size

    def on_click(self, cell_coords):
        if cell_coords is None:
            return
        x, y = cell_coords
        if type(self.board[y][x]) == Generator:
            self.board[y][x].generate()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Generator(pygame.sprite.Sprite):
    image = load_image('gen_veg.png')

    def __init__(self, group, _board, x, y):
        super().__init__(group)
        self.add(generators)
        self.add(movable_sprites)
        self.board = _board
        self.board_x = x
        self.board_y = y
        self.energy = 25
        self.image = Generator.image
        self.rect = self.image.get_rect()
        self.rect.x = self.board.rect.x + self.board_x * self.board.cell_size
        self.rect.y = self.board.rect.y + self.board_y * self.board.cell_size

    def generate(self):
        left, right = -1, 1
        dx_dy_list = [-1, 0, 1]
        while True:
            if right > self.board.width:
                return
            for dy in dx_dy_list:
                for dx in dx_dy_list:
                    if 0 <= self.board_x + dx < self.board.width and \
                            0 <= self.board_y + dy < self.board.height and \
                            self.board.board[self.board_y + dy][self.board_x + dx] == 0 and \
                            not (dy == 0 and dx == 0):
                        self.board.board[self.board_y + dy][self.board_x + dx] = (
                            Food(all_sprites, self.board, self.board_x + dx, self.board_y + dy))
                        return
            left, right = left - 1, right + 1
            dx_dy_list.append(left)
            dx_dy_list.append(right)
            dx_dy_list.sort()


class Food(pygame.sprite.Sprite):
    graduation = ['tomate.png', 'cucumber.png', 'carrot.png', 'peper.png', 'potato.png']

    def __init__(self, group, _board, x, y):
        super().__init__(group)
        self.add(foods)
        self.add(movable_sprites)
        self.board = _board
        self.board_x = x
        self.board_y = y
        self.energy = 25
        self.level_gr = random.randrange(2)
        self.image = load_image(Food.graduation[self.level_gr])
        self.rect = self.image.get_rect()
        self.rect.x = self.board.rect.x + self.board_x * self.board.cell_size
        self.rect.y = self.board.rect.y + self.board_y * self.board.cell_size


class Trash(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.add(trash_group)
        self.image = load_image('trash.png')
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 700


class Purpose(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.add(purpose_group)
        self.image = load_image('purpose.png')
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 10
        self.count = 3

    def draw_num(self):
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render(str(self.count), True, (0, 0, 0))
        const.screen.blit(self.text,
                         (350 + 300, 25))


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (20, 30, 40):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))
    fire = fire[1:]

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.add(stars_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


stars_group = pygame.sprite.Group()
def create_particles(position):
    particle_count = 15
    numbers = range(-10, 10)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def terminate():
    pygame.quit()
    sys.exit()


def finale_screen(cnt):
    fps = 60
    clock_finale = pygame.time.Clock()
    fon = load_image('finale_bg.jpg')
    last_ticks = 0
    font = pygame.font.Font(None, 74)
    text = font.render(f'Вы сделали 3 картошки за {cnt} кликов!', True, (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        const.screen.blit(fon, (0, 0))
        const.screen.blit(text, (115, 935))
        if pygame.time.get_ticks() - last_ticks > 300:
            create_particles((200, 300))
            create_particles((1000, 300))
            last_ticks = pygame.time.get_ticks()
        stars_group.draw(const.screen)
        pygame.display.flip()
        stars_group.update()
        clock_finale.tick(fps)


def handler_event(event):
    global take, sprite_take, take_pos, trash_group, purpose_group, purpose, game_over, click_count
    if event.type == pygame.MOUSEBUTTONDOWN:
        click_count += 1
        if event.button == pygame.BUTTON_LEFT:
            board.get_click(event.pos)
        elif event.button == pygame.BUTTON_RIGHT and board.get_cell(event.pos):
            x_, y_ = board.get_cell(event.pos)
            if board.board[y_][x_] != 0:
                take_pos = event.pos
                take = True
                sprite_take = board.board[y_][x_]
    if event.type == pygame.MOUSEMOTION and take:
        dx_ = event.pos[0] - take_pos[0]
        dy_ = event.pos[1] - take_pos[1]
        sprite_take.rect.x += dx_
        sprite_take.rect.y += dy_
        take_pos = [take_pos[0] + dx_, take_pos[1] + dy_]
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_RIGHT:
            if board.get_cell(event.pos) and sprite_take:
                x_, y_ = board.get_cell(event.pos)
                if board.board[y_][x_] == 0:
                    board.board[sprite_take.board_y][sprite_take.board_x] = 0
                    sprite_take.rect.x = board.rect.x + board.cell_size * x_
                    sprite_take.rect.y = board.rect.y + board.cell_size * y_
                    sprite_take.board_x = x_
                    sprite_take.board_y = y_
                    board.board[sprite_take.board_y][sprite_take.board_x] = sprite_take
                elif type(board.board[y_][x_]) == type(sprite_take) == Food and \
                        sprite_take.level_gr == board.board[y_][x_].level_gr and \
                        sprite_take.level_gr < len(Food.graduation) - 1 and \
                        not (sprite_take.board_x == x_ and sprite_take.board_y == y_):
                    board.board[sprite_take.board_y][sprite_take.board_x] = 0
                    board.board[y_][x_].kill()
                    board.board[y_][x_] = 0
                    sprite_take.rect.x = board.rect.x + board.cell_size * x_
                    sprite_take.rect.y = board.rect.y + board.cell_size * y_
                    sprite_take.level_gr += 1
                    sprite_take.image = load_image(Food.graduation[sprite_take.level_gr])
                    sprite_take.board_x = x_
                    sprite_take.board_y = y_
                    board.board[sprite_take.board_y][sprite_take.board_x] = sprite_take
                elif sprite_take:
                    sprite_take.rect.x = board.rect.x + board.cell_size * sprite_take.board_x
                    sprite_take.rect.y = board.rect.y + board.cell_size * sprite_take.board_y
            else:
                if sprite_take:
                    if pygame.sprite.spritecollideany(sprite_take, trash_group) and type(sprite_take) != Generator:
                        board.board[sprite_take.board_y][sprite_take.board_x] = 0
                        sprite_take.kill()
                    elif pygame.sprite.spritecollideany(sprite_take, purpose_group) and type(sprite_take) == Food and \
                        sprite_take.level_gr == 4:
                        purpose.count -= 1
                        board.board[sprite_take.board_y][sprite_take.board_x] = 0
                        sprite_take.kill()
                        if purpose.count == 0:
                            game_over = True
                            finale_screen(click_count)
                    else:
                        sprite_take.rect.x = board.rect.x + board.cell_size * sprite_take.board_x
                        sprite_take.rect.y = board.rect.y + board.cell_size * sprite_take.board_y
        take = False
        sprite_take = None


def init():
    global sprite_take, take, bg, board, clock, all, all_sprites, board_group, generators, foods, movable_sprites,\
        trash_group, trash, purpose, purpose_group, game_over, screen_rect, click_count
    _size = _width, _height = 1200, 1000
    const.screen = resize_screen(*_size)
    screen_rect = (0, 0, _width, _height)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    board_group = pygame.sprite.Group()
    generators = pygame.sprite.Group()
    foods = pygame.sprite.Group()
    movable_sprites = pygame.sprite.Group()
    trash_group = pygame.sprite.Group()
    purpose_group = pygame.sprite.Group()


    bg = load_image('kitchen.png')
    trash = Trash(all_sprites)
    purpose = Purpose(all_sprites)
    board = Board(all_sprites, 8, 8)
    take = False
    sprite_take = None
    game_over = False
    click_count = 0


def post_loop_step():
    global all_sprites, bg, purpose
    const.screen.blit(bg, (0, 0))
    all_sprites.draw(const.screen)
    purpose.draw_num()
    pygame.display.flip()
    all_sprites.update()
