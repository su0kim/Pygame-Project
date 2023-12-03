from pygame import Rect, Surface, draw, Color
from system.config import SNAKE_COLOR, SNAKE_WIDTH, SNAKE_HEIGHT, SNAKE_HEAD
from framework import *


class Snake:
    def __init__(self, left=0, top=0):
        self.count = 1
        self.body = [Tail(Point(left, top))]
        self.dir = Point(1, 0)

    @property
    def face(self):
        img = pygame.image.load(SNAKE_HEAD)
        angle = 0

        if self.dir == DIR_RIGHT:
            angle = -90

        elif self.dir == DIR_LEFT:
            angle = 90

        elif self.dir == DIR_DOWN:
            angle = 180

        img = img.convert_alpha()
        return pygame.transform.rotate(img, angle)

    @property
    def head(self):
        return self.body[0]

    @property
    def tails(self):
        return self.body[1:]

    @property
    def length(self):
        return len(self.body)

    def move(self) -> None:
        offset = self.dir * (self.head.size)

        for rect in self.body:
            new_pos = rect.position.copy()
            if rect == self.head:
                rect.move_by(offset)
            else:
                rect.move_to(pos)
            pos = new_pos.copy()

    def set_dir(self, dir: Point) -> None:
        if self.length > 1 and dir == -self.dir:
            return
        self.dir = dir

    def grow(self, position: Point) -> None:
        new_head = Tail(position)
        self.body.insert(0, new_head)

    def is_twist(self) -> bool:
        return any([self.head.rect.colliderect(tail.rect) for tail in self.tails])

    def Render(
        self,
        screen: Surface,
        width: int = 0,
        width_color: tuple[int, int, int] = (0, 0, 0),
        border_radius: int = 0,
        gradient: float = 0.0,
    ) -> None:
        """그림을 그린다."""
        for idx, tail in enumerate(self.body):
            if not idx:  # 머리 일때
                screen.blit(self.face, self.head.position.coord)

            else:
                tail.scale = self.body[idx - 1].scale * (1 - gradient)
                tail.Render(screen, width, width_color, border_radius)


class Tail:
    def __init__(self, topleft: Point) -> None:
        self.rect = Rect(topleft.coord, (SNAKE_WIDTH, SNAKE_HEIGHT))
        self.scale = 0.95
        self.size = Point(SNAKE_WIDTH, SNAKE_HEIGHT)
        self.color = SNAKE_COLOR

    @property
    def position(self) -> Point:
        return Point(*self.rect.topleft)

    @property
    def real(self) -> Rect:
        real_size = self.size * self.scale
        real_pos = Point(*self.rect.center) - (real_size / 2)
        return Rect(real_pos.coord, real_size.coord)

    def move_by(self, offset: Point):
        self.rect.move_ip(*offset.coord)

    def move_to(self, position: Point):
        self.rect.update(position.coord, self.size.coord)

    def Render(
        self,
        screen: Surface,
        width: int = 0,
        width_color: tuple[int, int, int] = (0, 0, 0),
        border_radius: int = 0,
    ):
        draw.rect(screen, self.color, self.real, 0, border_radius)

        if width:
            draw.rect(screen, Color(width_color), self.real, width, border_radius)
