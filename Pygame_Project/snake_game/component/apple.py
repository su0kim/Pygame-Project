from pygame import Rect
from framework import *
from system.config import APPLE_COLOR, APPLE_WIDTH, APPLE_HEIGHT
import pygame.draw as draw


class Apple:
    def __init__(self, position: Point):
        self.rect = Rect(position.coord, (APPLE_WIDTH, APPLE_HEIGHT))
        self.size = Point(APPLE_WIDTH, APPLE_HEIGHT)
        self.color = APPLE_COLOR

    @property
    def position(self):
        return Point(*self.rect.topleft)

    def Render(self, screen):
        draw.rect(screen, self.color, self.rect, 0, border_radius=10)
