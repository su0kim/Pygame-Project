from pygame.font import Font
from pygame import Surface

from .constant import EnumAlign, DEF_COLOR
from .utils import Point


class Text:
    def __init__(self, msg: str, font: Font, color: str = DEF_COLOR):
        self.msg = msg
        self.font = font
        self.color = color
        self.scale = 1
        self.size = Point(*self.surface.get_bounding_rect().size)

    @property
    def surface(self):
        return self.font.render(self.msg, True, self.color)

    def set_msg(self, msg: str):
        self.msg = msg

    def set_color(self, color: str):
        self.color = color

    def set_font(self, font):
        self.font = font

    def Render(
        self, screen: Surface, position: Point, align: EnumAlign = EnumAlign.TOPLEFT
    ):
        if not isinstance(align, EnumAlign):
            raise Exception("align arg must be EnumAlign")

        new_position = position.copy()

        if "center".upper() in align.name:
            new_position.x -= self.size.x / 2

        if "middle".upper() in align.name:
            new_position.y -= self.size.y / 2

        if "right".upper() in align.name:
            new_position.x -= self.size.x

        if "bot".upper() in align.name:
            new_position.y -= self.size.y

        screen.blit(self.surface, new_position.coord)
