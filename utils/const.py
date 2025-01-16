from pygame.surface import Surface, SurfaceType

POST_LOOP_STEP = lambda: ...  # функция, которая вызывается после каждого шага цикла
HANDLER_EVENT = lambda evevnt: ...  # функция обработчик событий

SCREEN_WIDTH = 700  # ширина экрана
SCREEN_HEIGHT = 350 # высота экрана

SIZE = width, height = SCREEN_WIDTH, SCREEN_HEIGHT

screen: Surface | SurfaceType = None  # экран