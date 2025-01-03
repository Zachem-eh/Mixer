import pygame
import os
import sys


pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
board_group = pygame.sprite.Group()


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
        self.cell_size = screen.get_width() // (self.width + 1)
        self.image = pygame.Surface((self.width * self.cell_size, self.width * self.cell_size), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.cell_size // 2, self.cell_size // 2)
        self.board = [[0] * _width for _ in range(_height)]
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(self.image, 'white',(self.cell_size * x,
                                                   self.cell_size * y, self.cell_size, self.cell_size), 1)

    def update(self, *args):
        pass


board = Board(all_sprites, 10, 10)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
    all_sprites.draw(screen)
    pygame.display.flip()
    all_sprites.update()

pygame.quit()
