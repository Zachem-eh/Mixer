from typing import Optional

from pygame.surface import Surface, SurfaceType

from games.base import GameObjectsMap

POST_LOOP_STEP = lambda: ...  # функция, которая вызывается после каждого шага цикла
HANDLER_EVENT = lambda evevnt: ...  # функция обработчик событий

SCREEN_WIDTH = 700  # ширина экрана
SCREEN_HEIGHT = 700  # высота экрана

GAMES_MAP: GameObjectsMap | None = None

SIZE = width, height = SCREEN_WIDTH, SCREEN_HEIGHT

screen: Surface | SurfaceType | None = None  # экран

CURRENT_USER: Optional[str] = None

PAUSE = False
