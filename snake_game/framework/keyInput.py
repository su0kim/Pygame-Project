import pygame

UP = pygame.K_w, pygame.K_UP
DOWN = pygame.K_s, pygame.K_DOWN
LEFT = pygame.K_a, pygame.K_LEFT
RIGHT = pygame.K_d, pygame.K_RIGHT

PAUSE = pygame.K_SPACE
RESTART = pygame.K_SPACE
QUIT = pygame.K_ESCAPE

LCLICK = 0
RCLICK = 1
MCLICK = 2

WHEELUP = pygame.BUTTON_WHEELUP
WHEELDOWN = pygame.BUTTON_WHEELDOWN


def KeyInput(keys) -> bool:
    """키 입력을 확인한다. 중복 키 가능, 키가 없을 경우 항상 True"""
    if not keys:
        return True

    if isinstance(keys, int):
        keys = [keys]

    return any([pygame.key.get_pressed()[key] for key in keys])


def MouseInput(key) -> bool:
    return pygame.mouse.get_pressed()[key]


def Is_MouseOver(obj: pygame.Rect) -> bool:
    point = pygame.mouse.get_pos()

    if isinstance(obj, pygame.Rect):
        return obj.collidepoint(point)
