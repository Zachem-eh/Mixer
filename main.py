import time

import pygame

from games import base
from utils import const, tools
from utils.tools import _handler_event_next_game

pygame.init()
const.screen = pygame.display.set_mode(const.SIZE)  # временный скрин

games_map = base.load_games()
const.GAMES_MAP = games_map
const.START_TIME = time.time()

games_map.run_game(name='start_screen')

running = True
while running:
    if not pygame.get_init():
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_5:
                tools.restart_game()
            elif event.key == pygame.K_4:
                tools.lvl_passed()  # преждевременное прохождение
            else:
                const.HANDLER_EVENT(event)
        else:
            res = _handler_event_next_game(event)
            if not res and not const.WAIT_NEXT_GAME:
                const.HANDLER_EVENT(event)

    const.POST_LOOP_STEP()
