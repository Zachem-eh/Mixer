import random

import pygame

from utils import const
from utils.const import height
from utils.tools import load_image, resize_screen, lvl_passed

PIPE_WIDTH = 80
PIPE_HEIGHT = 300
PIPES_COUNT = 5
LIGHTNING_SIZE = 40
BIRD_SPEED = 0.5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 550


class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("bird.png", -1)
        self.rect = self.image.get_rect(center=(100, height // 2))
        self.mask = pygame.mask.from_surface(self.image)
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
        self.mask = pygame.mask.from_surface(self.image)


class Lightning(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = load_image("lightning2.png", -1)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


def init():
    global all_sprites, pipes, lightnings, bird, game_over, collected_lightning, clock, start_game_update
    pygame.display.set_caption("Flappy Bird")
    all_sprites = pygame.sprite.Group()
    pipes = pygame.sprite.Group()
    lightnings = pygame.sprite.Group()
    start_game_update = False

    size = 1000, 550
    const.screen = resize_screen(*size)

    bird = Bird(all_sprites)

    def create_static_pipes():
        previous_gap_center = random.randint(200, 350)
        for i in range(PIPES_COUNT):
            x = 200 + i * (PIPE_WIDTH + 50)
            gap = random.randint(150, 200)
            gap_center = previous_gap_center + random.randint(-50, 50)
            gap_center = max(100 + gap // 2, min(height - 100 - gap // 2, gap_center))

            top_pipe = Pipe(x, gap_center - gap // 2, True, all_sprites, pipes)
            bottom_pipe = Pipe(x, gap_center + gap // 2, False, all_sprites, pipes)
            previous_gap_center = gap_center

    def create_lightning():
        x = 900
        y = random.randint(250, height - 250)
        Lightning(x, y, all_sprites, lightnings)

    create_static_pipes()
    create_lightning()

    clock = pygame.time.Clock()
    game_over = False
    collected_lightning = False


def handler_event(event):
    global bird, start_game_update
    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start_game_update = True
            bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_game_update = True
            bird.jump()


def post_loop_step():
    global game_over, collected_lightning, start_game_update
    const.screen.fill((135, 206, 235))

    if not game_over and start_game_update:
        if pygame.sprite.spritecollide(bird, pipes, False, pygame.sprite.collide_mask):
            game_over = True

        if pygame.sprite.spritecollide(bird, lightnings, True, pygame.sprite.collide_mask):
            collected_lightning = True

        if not bird.alive() or bird.rect.right > SCREEN_WIDTH:
            game_over = True

        all_sprites.update()

    all_sprites.draw(const.screen)
    if not start_game_update:
        font = pygame.font.Font(None, 74)
        text = font.render("Press SPACE to start", True, (255, 0, 0))
        text_rect = text.get_rect(center=(const.screen.get_width() // 2, const.screen.get_height() // 2))
        const.screen.blit(text, text_rect)

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render('Game over. Tap to "5" for restart', True, (255, 0, 0))
        const.screen.blit(text,
                          (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    elif collected_lightning:
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (0, 255, 0))
        const.screen.blit(text,
                          (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        return lvl_passed()

    pygame.display.flip()
    clock.tick(60)
