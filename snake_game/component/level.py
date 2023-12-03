from typing import List

import pygame
from system.config import *
from framework import *
from .snake import Snake
from .apple import Apple

import itertools as it
import random


class Level:
    def __init__(self, left: int, top: int, width: int, height: int):
        self.canvas = pygame.Rect((left, top), (width, height))
        self.size = Point(width, height)
        self.color = "white"
        self.snake = Snake(self.canvas.left, self.canvas.top)
        self.apple: Apple = None

        self.map = self.create_map()

    def create_map(self) -> List[Point]:
        """레벨을 구성하는 맵"""
        Map = []
        for x, y in it.product(
            range(int(self.size.x / self.snake.head.size.x)),
            range(int(self.size.y / self.snake.head.size.y)),
        ):
            pt = Point(
                x * self.snake.head.size.x + self.canvas.left,
                y * self.snake.head.size.y + self.canvas.top,
            )
            Map.append(pt)
        return Map

    @property
    def empty_spaces(self) -> List[Point]:
        """레벨 상의 빈 공간"""
        empty_spaces = []

        for pt in self.map:
            if pt not in [tail.position for tail in self.snake.body]:
                empty_spaces.append(pt)

        return empty_spaces

    def generate_apple(self):
        if self.apple:
            return

        position = random.choice(self.empty_spaces)
        self.apple = Apple(position)

    def is_conflict(self) -> bool:
        """맵과의 충돌을 체크한다."""
        head = self.snake.head.rect
        if (
            head.top < self.canvas.top
            or head.bottom > self.canvas.bottom
            or head.left < self.canvas.left
            or head.right > self.canvas.right
        ):
            return True

        if self.snake.is_twist():
            return True

        return False

    def eat_apple(self):
        """사과와 닿으면 먹는다."""
        head = self.snake.head.rect
        if head.colliderect(self.apple.rect):
            self.snake.grow(self.apple.position)
            self.apple = None

    def Render(self, screen=pygame.Surface):
        pygame.draw.rect(screen, self.color, self.canvas, 1)
