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
    next_lvl = db.next_lvl(const.CURRENT_USER)
    const.GAMES_MAP.run_game(next_lvl)


def restart_game():
    const.GAMES_MAP.run_game(
        db.get_user(const.CURRENT_USER).curr_lvl
    )
