import os
import sys
import random
import pygame

pygame.init()

BIRD_SIZE = 40
PIPE_WIDTH = 60
PIPE_HEIGHT = 106
GAP = 150
PIPES_COUNT = 6
LIGHTNING_SIZE = 40
BIRD_SPEED = 0.5


SCREEN_WIDTH = PIPES_COUNT * (PIPE_WIDTH + 50) + 400
SCREEN_HEIGHT = 350

size = width, height = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")

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


all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
lightnings = pygame.sprite.Group()

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
running = True
game_over = False
collected_lightning = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bird.jump()

    screen.fill((135, 206, 235))

    if not game_over:
        if pygame.sprite.spritecollide(bird, pipes, False):
            game_over = True

        if pygame.sprite.spritecollide(bird, lightnings, True):
            collected_lightning = True

        if not bird.alive() or bird.rect.right > SCREEN_WIDTH:
            game_over = True

        all_sprites.update()

    all_sprites.draw(screen)

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    elif collected_lightning:
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (0, 255, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
