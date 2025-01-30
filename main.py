import pygame
from utils import const, tools
from games import base


timer = 0


def start_everything():
    global timer
    pygame.init()
    const.screen = pygame.display.set_mode(const.SIZE) # временный скрин

    games_map = base.load_games()
    const.GAMES_MAP = games_map

    games_map.run_game(name='mixer')

    running = True
    while running:
        timer_1 = pygame.time.get_ticks()
        timer = timer_1
        print(timer)
        if not pygame.get_init():
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                tools.restart_game()
            else:
                const.HANDLER_EVENT(event)

        const.POST_LOOP_STEP()


if __name__ == '__main__':
    start_everything()
