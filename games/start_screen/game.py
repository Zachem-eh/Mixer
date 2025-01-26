import pygame
from utils.db import db
from utils import const
from animations.shaurma import add_animation

FPS = 10
WIDTH, HEIGHT = size = 1000, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

def enter_name(nickname):
    """
    Запуск игры maze после нажатия Enter
    """
    user = db.new_user(nickname)
    const.CURRENT_USER = nickname
    const.GAMES_MAP.run_game(user.curr_lvl)

FUNC = enter_name

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text_color = pygame.Color('black')
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.text_color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text:
                        if FUNC:
                            FUNC(self.text)
                        self.text = ''
                    else:
                        error_message = pygame.font.Font(None, 36).render("Введите логин чтобы продолжить, а затем нажмите Enter", True, (255, 0, 0))
                        screen.blit(error_message, (WIDTH // 2 - error_message.get_width() // 2, HEIGHT // 2 + 100))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.text_color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, _screen):
        _screen.fill(self.color, self.rect)
        _screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(_screen, (255, 255, 255), self.rect, 2)

def init():
    global input_box
    input_box = InputBox(WIDTH // 2 - 250, HEIGHT // 2 - 100, 500, 32)
    add_animation(all_sprites)

def handler_event(event):
    input_box.handle_event(event)

def post_loop_step():
    screen.fill('white')
    font = pygame.font.Font(None, 36)
    text = font.render("Введите логин чтобы продолжить, а затем нажмите Enter", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))  # Центрирование текста по горизонтали
    input_box.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)