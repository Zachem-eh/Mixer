import random

import pygame

from utils import const
from utils.const import height, width, SCREEN_WIDTH
from utils.tools import load_image

BIRD_SIZE = 40
PIPE_WIDTH = 60
PIPE_HEIGHT = 106
GAP = 150
PIPES_COUNT = 6
LIGHTNING_SIZE = 40
BIRD_SPEED = 0.5


class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("bird.png", -1)
        self.image = pygame.transform.scale(self.image, (BIRD_SIZE, BIRD_SIZE))
        self.rect = self.image.get_rect(center=(100, height // 2))
        self.gravity = 0
        self.jump_speed = -5

    def update(self):
        self.gravity += 0.25
        self.rect.y += self.gravity
        self.rect.x += BIRD_SPEED
        if self.rect.top < 0 or self.rect.bottom > height:
            self.kill()

    def jump(self):
        self.gravity = self.jump_speed


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top, *groups):
        super().__init__(*groups)
        self.image = load_image("pipe.png", -1)
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        if is_top:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(midtop=(x, y) if not is_top else (x, y - self.image.get_height()))


class Lightning(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = load_image("lightning.png", -1)
        self.image = pygame.transform.scale(self.image, (LIGHTNING_SIZE, LIGHTNING_SIZE))
        self.rect = self.image.get_rect(center=(x, y))


def init():
    global all_sprites, pipes, lightnings, bird, game_over, collected_lightning, clock
    pygame.display.set_caption("Flappy Bird")
    all_sprites = pygame.sprite.Group()
    pipes = pygame.sprite.Group()
    lightnings = pygame.sprite.Group()

    size = PIPES_COUNT * (PIPE_WIDTH + 50) + 400, 350
    const.screen = pygame.display.set_mode(size)

    bird = Bird(all_sprites)

    def create_static_pipes():
        for i in range(PIPES_COUNT):
            x = 200 + i * (PIPE_WIDTH + 50)
            gap_center = random.randint(150, height - 150)
            top_pipe = Pipe(x, gap_center - GAP // 2, True, all_sprites, pipes)
            bottom_pipe = Pipe(x, gap_center + GAP // 2, False, all_sprites, pipes)

    def create_lightning():
        x = 200 + PIPES_COUNT * (PIPE_WIDTH + 50) + 50
        y = random.randint(100, height - 100)
        Lightning(x, y, all_sprites, lightnings)

    create_static_pipes()
    create_lightning()

    clock = pygame.time.Clock()
    game_over = False
    collected_lightning = False


def handler_event(event):
    global bird
    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bird.jump()


def post_loop_step():
    global game_over, collected_lightning
    const.screen.fill((135, 206, 235))

    if not game_over:
        if pygame.sprite.spritecollide(bird, pipes, False):
            game_over = True

        if pygame.sprite.spritecollide(bird, lightnings, True):
            collected_lightning = True

        if not bird.alive() or bird.rect.right > SCREEN_WIDTH:
            game_over = True

        all_sprites.update()

    all_sprites.draw(const.screen)

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        const.screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    elif collected_lightning:
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (0, 255, 0))
        const.screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)
