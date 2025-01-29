import logging
import os
import time
from importlib import import_module

import pygame

from utils import const
from utils.db import db

log = logging.getLogger(__name__)


"""

Чтобы создать игру, нужно создать папку в /games
В папке с игрой создать файл game.py, туда поместить код игры, а именно

    init: функция которая будет инициализировать игру (вызывается первая)
    post_loop_step: функция которая будет вызываться каждый шаг в цикле
    handler_event: функция которая будет обрабатывать эвент
    
экран (screen) импортировать из utils.const:

    from utils import cosnt
    screen = const.screen
    
"""

exclude_folders = [
    'animations'
]


def load_games(dirname: str = "games") -> 'GameObjectsMap':
    """
    Загружает все игры из указанной папки
    Args:
        dirname: путь к папке с играми
    Returns:
    """
    all_games = {}
    for game_dir in os.listdir(dirname):
        if game_dir.startswith("_") or "." in game_dir or game_dir in exclude_folders:
            continue
        try:
            all_games[game_dir] = _load_game(game_dir)
        except Exception as e:
            log.exception(f"Ошибка при загрузке игры {game_dir}: {str(e)}")
    return GameObjectsMap(all_games)


def _load_game(path):
    """
    Загружает (импортирует) игру
    Args:
        path: путь к папке с игрой (название папки)
    """
    _module_game = import_module(f"games.{path}.game")
    for attr in ("post_loop_step", "handler_event", "init"):
        if not hasattr(_module_game, attr):
            raise ValueError(f'Не найдено поле "{attr}" в игре {path}')
    init_func = _module_game.init if hasattr(_module_game, "init") else None
    return GameObject(
        _module_game,
        path,
        _module_game.post_loop_step,
        _module_game.handler_event,
        init_func
    )

class GameObjectsMap:
    """
    Класс для хранения игр
    """
    def __init__(
        self,
        games: dict[str, 'GameObject'] = {}
    ):
        self.games = games

    def __iter__(self):
        return iter(self.games.values())

    def __getitem__(self, index):
        return list(self.games.values())[index]

    def run_game(self, index: int = 1, name=None):
        """
        Запускает игру по индексу
        По умолчанию, это первая игра

        Загружаются игры в алфавитном порядке!
        """
        db.update_user(const.CURRENT_USER, start_time=time.time())
        if not name:
            game = list(self.games.values())[index - 1]
            if game.name == "start_screen":  # по индексу нельзя запустить стартовый экран
                return
            game.show()
        else:
            game = next((g for g in self.games.values() if g.name == name), None)
            if game:
                game.show()
            else:
                raise Exception("Game not found")

class GameObject:
    """
    Класс игры

    Attributes:
        module: Модуль игры, то же самое что "import {модуль}"
        name: Название игры
        post_loop_step: Функция вызываемая в конце каждого шага цикла
        handler_event: Функция, обрабатывает нажатия
        init_func: Функция инициализации игры
    """
    def __init__(
        self,
        module,
        name,
        post_loop_step,
        handler_event,
        init_func
    ):
        self.module = module
        self.name = name
        self.post_loop_step = post_loop_step
        self.handler_event = handler_event
        self.init_func = init_func

    def set_main(self):
        """
        Устанавливает обработчики нажатий на клавиши
        """
        const.HANDLER_EVENT = self.handler_event
        const.POST_LOOP_STEP = self.post_loop_step

    def init(self):
        """
        Инициализирует игру.
        """
        self.init_func()
        self.post_loop_step()

    def show(self):
        """
        Функция запускает игру (устанавливает обработчики нажатий и показывает на экране)

        Можно вызывать при переключении игр, например
        """
        self.set_main()
        self.init()
