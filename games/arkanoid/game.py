import random

import pygame

from utils import const
from utils.tools import load_image


class Platform(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.add(platform_group)
        self.image = pygame.Surface((100, 20), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, 'blue', (0, 0, 100, 20))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        if args:
            if args[0] == pygame.K_LEFT and self.rect.x - 10 >= 0:
                self.rect = self.rect.move(-10, 0)
            elif args[0] == pygame.K_RIGHT and self.rect.x + 10 + self.rect.width <= const.screen.get_width():
                self.rect = self.rect.move(10, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-10,-5)
        self.vy = random.randrange(-10, -5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, platform_group):
            self.vy = -self.vy
        elif not self.rect.colliderect(screen_rect):
                    self.kill()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.add(blocks)
        self.image = pygame.Surface((100, 20), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, 'black', (0, 0, 100, 20))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


def handler_event(event):
    global press
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            press = [True, event.key]
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            press = [False, None]

def init():
    global clock, all_sprites, screen_rect, platform_group, horizontal_borders, vertical_borders, blocks, fps, \
        platform, ball, press
    _size = _width, _height = 1200, 1000
    const.screen = pygame.display.set_mode(_size)

    screen_rect = (0, 0, _width, _height)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    fps = 30

    Border(5, 5, const.screen.get_width() - 5, 5)
    Border(5, 5, 5, const.screen.get_height() - 5)
    Border(const.screen.get_width() - 5, 5, const.screen.get_width() - 5, const.screen.get_height() - 5)
    Block(all_sprites, (const.screen.get_width() // 2 - 50, const.screen.get_height() // 2 - 10))
    platform = Platform(all_sprites, (const.screen.get_width() // 2 - 50, const.screen.get_height() * 3 / 4))
    ball = Ball(20, const.screen.get_width() // 2, const.screen.get_height() // 2)
    press = [False, None]


def post_loop_step():
    global all_sprites, fps, clock
    const.screen.fill('black')
    all_sprites.draw(const.screen)
    pygame.display.flip()
    all_sprites.update()
    if press[0]:
        platform.update(press[1])
    clock.tick(fps)


