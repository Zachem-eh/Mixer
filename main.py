import pygame
import os
import sys
import random

pygame.init()
size = width, height = 1200, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
board_group = pygame.sprite.Group()
generators = pygame.sprite.Group()
foods = pygame.sprite.Group()
movable_sprites = pygame.sprite.Group()


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


class Board(pygame.sprite.Sprite):
    def __init__(self, group, _width, _height):
        super().__init__(group)
        board_group.add(self)
        self.width = _width
        self.height = _height
        self.cell_size = screen.get_width() // (self.width + 10)
        self.image = pygame.Surface((self.width * self.cell_size, self.width * self.cell_size), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((screen.get_width() - self.cell_size * self.width) / 2,
                                   (screen.get_height() - self.cell_size * self.height) / 1.8)
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
        generators.add(self)
        movable_sprites.add(self)
        self.board = _board
        self.board_x = x
        self.board_y = y
        self.energy = 25
        self.image = Generator.image
        self.rect = self.image.get_rect()
        self.rect.x = self.board.rect.x + self.board_x * self.board.cell_size
        self.rect.y = self.board.rect.y + self.board_y * self.board.cell_size

    def generate(self):
        if self.energy > 0:
            self.energy -= 1
            left, right = -1, 1
            dx_dy_list = [-1, 0, 1]
            while True:
                if right > self.board.width:
                    return
                for dy in dx_dy_list:
                    for dx in dx_dy_list:
                        if 0 <= self.board_x + dx < self.board.width and\
                                0 <= self.board_y + dy < self.board.height and\
                                self.board.board[self.board_y + dy][self.board_x + dx] == 0 and\
                                not (dy == 0 and dx == 0):
                                self.board.board[self.board_y + dy][self.board_x + dx] =(
                                    Food(all_sprites, self.board, self.board_x + dx, self.board_y + dy))
                                return
                left, right = left - 1, right + 1
                dx_dy_list.append(left)
                dx_dy_list.append(right)
                dx_dy_list.sort()
        else:
            self.energy = 25


class Food(pygame.sprite.Sprite):
    graduation = ['tomate.png', 'cucumber.png', 'carrot.png', 'peper.png', 'potato.png']

    def __init__(self, group, _board, x, y):
        super().__init__(group)
        foods.add(self)
        movable_sprites.add(self)
        self.board = _board
        self.board_x = x
        self.board_y = y
        self.energy = 25
        self.level_gr = random.randrange(2)
        self.image = load_image(Food.graduation[self.level_gr])
        self.rect = self.image.get_rect()
        self.rect.x = self.board.rect.x + self.board_x * self.board.cell_size
        self.rect.y = self.board.rect.y + self.board_y * self.board.cell_size


bg = load_image('kitchen.png')
board = Board(all_sprites, 8, 8)
take = False
sprite_take = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
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
                    else:
                        if sprite_take:
                            sprite_take.rect.x = board.rect.x + board.cell_size * sprite_take.board_x
                            sprite_take.rect.y = board.rect.y + board.cell_size * sprite_take.board_y
                else:
                    if sprite_take:
                        sprite_take.rect.x = board.rect.x + board.cell_size * sprite_take.board_x
                        sprite_take.rect.y = board.rect.y + board.cell_size * sprite_take.board_y
            take = False
            sprite_take = None
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    all_sprites.update()

pygame.quit()
