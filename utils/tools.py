import logging
import os
import time

import pygame

from . import const
from .db import db

logger = logging.getLogger(__name__)


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


def _handler_event_next_game(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
        lvl_passed(showed_game_over=False)
        return 1
    return 0


def resize_screen(new_width, new_height):
    pygame.quit()
    pygame.init()
    const.screen = pygame.display.set_mode((new_width, new_height))
    return const.screen


def lvl_passed(showed_game_over=True):
    logger.info("Lvl passed func")
    if showed_game_over:
        const.WAIT_NEXT_GAME = True
        add_text(
            f'Lvl completed after {round(time.time() - db.get_user(const.CURRENT_USER).start_time, 2)}. Press "Enter" for go to next lvl')
        return
    const.WAIT_NEXT_GAME = False
    next_lvl = db.next_lvl(const.CURRENT_USER)
    const.GAMES_MAP.run_game(next_lvl)


def restart_game():
    const.WAIT_NEXT_GAME = False
    const.GAMES_MAP.run_game(
        db.get_user(const.CURRENT_USER).curr_lvl
    )


def add_text(string):
    _SCREEN_HEIGHT, _SCREEN_WIDTH = const.screen.get_size()
    font = pygame.font.Font(None, 74)
    text = font.render(string, True, (255, 0, 0))
    const.screen.blit(text, (_SCREEN_WIDTH // 2 - text.get_width() // 2, _SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
