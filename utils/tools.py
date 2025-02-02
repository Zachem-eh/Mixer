import time

import pygame
import os
from . import const
from .db import db


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        raise Exception(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def resize_screen(new_width, new_height):
    pygame.quit()
    pygame.init()
    const.screen = pygame.display.set_mode((new_width, new_height))
    return const.screen


def lvl_passed():
    result = time.time() - db.get_user(const.CURRENT_USER).start_time
    add_text(f'Пройдено за {round(result, 2)} секунд. Продолжить - "Enter"')
    const.READY_NEXT = True
    const.POST_LOOP_STEP = lambda: ...

def next_game():
    next_lvl = db.next_lvl(const.CURRENT_USER)
    const.GAMES_MAP.run_game(next_lvl)
    const.READY_NEXT = False


def restart_game():
    const.GAMES_MAP.run_game(
        db.get_user(const.CURRENT_USER).curr_lvl
    )

def add_text(text, size=50):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, (255, 0, 0))
    text_rect = text.get_rect(center=(const.screen.get_width() // 2, const.screen.get_height() // 2))
    const.screen.blit(text, text_rect)
    pygame.display.flip()
