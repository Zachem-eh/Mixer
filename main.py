import pygame
from utils import const
from games import base

pygame.init()
games_map = base.load_games()

games_map.run_game(0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            const.HANDLER_EVENT(event)

    const.POST_LOOP_STEP()