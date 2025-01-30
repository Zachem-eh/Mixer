import random
import pygame
from utils import const, tools
from utils.tools import load_image

game_over = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.add(platform_group)
        self.image = pygame.Surface((100, 20), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, 'blue', (0, 0, 100, 20))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.border_left = Border(pos[0], pos[1] + 2, pos[0], pos[1] + self.rect.height - 2)
        self.border_right = Border(pos[0] + self.rect.width - 2, pos[1] + 2, pos[0] + self.rect.width - 2, pos[1] +
                                   self.rect.height - 2)
        self.border_up = Border(pos[0] + 2, pos[1], pos[0] + self.rect.width - 2, pos[1])

    def update(self, *args):
        if args:
            if args[0] == pygame.K_LEFT and self.rect.x - 10 >= 0:
                self.rect = self.rect.move(-2, 0)
                self.border_left.rect = self.border_left.rect.move(-2, 0)
                self.border_right.rect = self.border_right.rect.move(-2, 0)
                self.border_up.rect = self.border_up.rect.move(-2, 0)
            elif args[0] == pygame.K_RIGHT and self.rect.x + 10 + self.rect.width <= const.screen.get_width():
                self.rect = self.rect.move(2, 0)
                self.border_left.rect = self.border_left.rect.move(2, 0)
                self.border_right.rect = self.border_right.rect.move(2, 0)
                self.border_up.rect = self.border_up.rect.move(2, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('ball.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = random.choice([-1, 1])
        self.vy = -1

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, blocks):
            spr_coll = pygame.sprite.spritecollideany(self, blocks)
            if pygame.sprite.spritecollideany(self, horizontal_borders) and \
                    pygame.sprite.spritecollideany(self, vertical_borders):
                hor_spr = pygame.sprite.spritecollideany(self, horizontal_borders)
                offset_hor = hor_spr.rect.x - self.rect.x, hor_spr.rect.y - self.rect.y
                ver_spr = pygame.sprite.spritecollideany(self, vertical_borders)
                offset_ver = ver_spr.rect.x - self.rect.x, ver_spr.rect.y - self.rect.y
                if self.mask.overlap_area(hor_spr.mask, offset_hor) > self.mask.overlap_area(ver_spr.mask, offset_ver):
                    self.vy = -self.vy
                elif self.mask.overlap_area(hor_spr.mask, offset_hor) < self.mask.overlap_area(ver_spr.mask, offset_ver):
                    self.vx = -self.vx
                else:
                    self.vy = -self.vy
                    self.vx = -self.vx
            elif pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            elif pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
            spr_coll.border_left.kill()
            spr_coll.border_right.kill()
            spr_coll.border_up.kill()
            spr_coll.border_down.kill()
            spr_coll.kill()
        if pygame.sprite.spritecollide(self, platform_group, False, pygame.sprite.collide_mask):
            if pygame.sprite.spritecollide(self, horizontal_borders, False, pygame.sprite.collide_mask):
                self.vy = -self.vy
            if pygame.sprite.spritecollide(self, vertical_borders, False, pygame.sprite.collide_mask):
                self.vx = -self.vx
        else:
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
        if not self.rect.colliderect(screen_rect):
            self.kill()
            global game_over
            game_over = True
            show_game_over()

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([2, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 2, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 2])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 2)
        self.mask = pygame.mask.from_surface(self.image)

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.add(blocks)
        self.image = pygame.Surface((100, 40), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, 'blue', (0, 0, 100, 40))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.border_left = Border(pos[0], pos[1] + 2, pos[0], pos[1] + self.rect.height - 2)
        self.border_right = Border(pos[0] + self.rect.width - 2, pos[1] + 2, pos[0] + self.rect.width - 2, pos[1] +
                                   self.rect.height - 2)
        self.border_up = Border(pos[0] + 2, pos[1], pos[0] + self.rect.width - 2, pos[1])
        self.border_down = Border(pos[0] + 2, pos[1] + self.rect.height - 2, pos[0] +
                                  self.rect.width - 2, pos[1] + self.rect.height - 2)

def show_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over. Tap 5 to restart", True, (255, 0, 0))
    text_rect = text.get_rect(center=(const.screen.get_width() // 2, const.screen.get_height() // 2))
    const.screen.blit(text, text_rect)
    pygame.display.flip()

def handler_event(event):
    global press
    if not game_over:
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
    const.screen = tools.resize_screen(*_size)

    screen_rect = (0, 0, _width, _height)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    fps = 150

    Border(5, 5, const.screen.get_width() - 5, 5)
    Border(5, 5, 5, const.screen.get_height() - 5)
    Border(const.screen.get_width() - 5, 5, const.screen.get_width() - 5, const.screen.get_height() - 5)
    platform = Platform(all_sprites, (const.screen.get_width() // 2 - 50, const.screen.get_height() * 3 / 4))
    ball = Ball(const.screen.get_width() // 2, const.screen.get_height() // 2)
    press = [False, None]
    y_0 = const.screen.get_height() // 20 * 4
    for y in range(5):
        y_0 += 41
        x_0 = (const.screen.get_width() / 100 - 10) / 2 * 100
        for x in range(10):
            Block(all_sprites, (x_0, y_0))
            x_0 += 101

def post_loop_step():
    global all_sprites, fps, clock, game_over
    const.screen.fill('white')
    all_sprites.draw(const.screen)
    pygame.display.flip()
    if not game_over:
        all_sprites.update()
        if press[0]:
            platform.update(press[1])
        if not blocks:
            game_over = True
            return tools.lvl_passed()
    clock.tick(fps)
