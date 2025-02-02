import pygame
from utils import const, tools
from games import base

pygame.init()
const.screen = pygame.display.set_mode(const.SIZE) # временный скрин

games_map = base.load_games()
const.GAMES_MAP = games_map

games_map.run_game(name='start_screen')

running = True
while running:
    if not pygame.get_init():
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
            tools.restart_game()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            tools.lvl_passed()
        elif const.READY_NEXT and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            tools.next_game()
        else:
            const.HANDLER_EVENT(event)

    const.POST_LOOP_STEP()