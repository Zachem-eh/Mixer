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
    image = load_image('veg.png')

    def __init__(self, group, _board, x, y):
        super().__init__(group)
        generators.add(self)
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
            while True:
                for dy in [left, 0, right]:
                    for dx in [left, 0, right]:
                        if 0 <= self.board_x + dx < self.board.width and\
                                0 <= self.board_y + dy < self.board.height and\
                                self.board.board[self.board_y + dy][self.board_x + dx] == 0 and\
                                not (dy == 0 and dx == 0):
                                print(self.board_y + dy, self.board_x + dx)
                                return
                left, right = left - 1, right + 1
        else:
            self.energy = 25
            pass


bg = load_image('kitchen.png')
board = Board(all_sprites, 8, 8)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    all_sprites.update()

pygame.quit()
