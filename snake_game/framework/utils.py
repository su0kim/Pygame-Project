from typing import List, Set, Dict
import math as math


class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    @property
    def origin(self):
        return Point()

    @property
    def size(self):
        return self.distance_to(self.origin)

    @property
    def coord(self) -> tuple[float, float]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return "{},{}".format(*self)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __neg__(self):
        # type: () -> Point
        return Point(self.x * -1, self.y * -1)

    def __add__(self, other):
        # type: (Point) -> Point
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        # type: (Point) -> Point
        return self + (-other)

    def __mul__(self, num):
        if isinstance(num, Point):
            return Point(self.x * num.x, self.y * num.y)
        return Point(self.x * num, self.y * num)

    def __truediv__(self, num):
        if isinstance(num, Point):
            return Point(self.x / num.x, self.y / num.y)
        return Point(self.x / num, self.y / num)

    def __eq__(self, other):
        # type: (Point) -> bool
        return self.x == other.x and self.y == other.y

    def copy(self):
        # type: () -> Point
        return Point(self.x, self.y)

    def distance_to(self, other):
        # type: (Point) -> float
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Polygon:
    def __init__(self, *vertice: Point):
        self.vertice = list(vertice)

    @property
    def coord(self) -> tuple[tuple[int, int]]:
        return tuple([vert.coord for vert in self.vertice])

    @property
    def bounding_rect(self):
        min_x = min([vert.x for vert in self.vertice])
        max_x = max([vert.x for vert in self.vertice])

        min_y = min([vert.y for vert in self.vertice])
        max_y = max([vert.y for vert in self.vertice])

        pt1 = Point(min_x, min_y)
        pt2 = Point(max_x, min_y)
        pt3 = Point(max_x, max_y)
        pt4 = Point(min_x, max_y)

        return Polygon(pt1, pt2, pt3, pt4)

    @property
    def center(self) -> Point:
        center = Point(0, 0)
        for vert in self.vertice:
            center += vert
        return center / len(self)

    def __repr__(self) -> str:
        string = ""
        for vert in self:
            string += "(" + str(vert) + ")"
            string += ", "
        string = string[:-2]
        return string

    def __iter__(self):
        return (vert for vert in self.vertice)

    def __add__(self, other):
        if isinstance(other, Point):
            vertice = self.vertice + [other]
            return Polygon(*vertice)

        elif isinstance(other, Polygon):
            vertice = self.vertice + other.vertice
            return Polygon(*vertice)

    def __len__(self):
        return len(self.vertice)

    def copy(self):
        return Polygon(*self)

    def invert(self, axis: int = 0):
        """반전한 폴리곤을 얻는다. axis:0 일 경우 좌우반전, 1일 경우 상하반전, 2일 경우 모두 반전"""
        new_vertices = []
        b_center = self.bounding_rect.center

        for vert in self.vertice:
            transform = b_center - vert
            mirror_vertice = vert + transform * 2

            if axis == 0:
                mirror_vertice = Point(mirror_vertice.x, vert.y)

            elif axis == 1:
                mirror_vertice = Point(vert.x, mirror_vertice.y)

            new_vertices.append(mirror_vertice)

        return Polygon(*new_vertices)

    def move_to(self, position: Point, snap_index: int = None):
        if snap_index == None:
            snap_pt = self.center
        else:
            snap_pt = self.vertice[snap_index]

        transform = position - snap_pt
        new_vertices = []

        for vert in self.vertice:
            vert += transform
            new_vertices.append(vert)

        return Polygon(*new_vertices)
