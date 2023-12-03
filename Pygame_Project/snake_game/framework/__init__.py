from .utils import Point, Polygon
from .constant import *
from .keyInput import *
from .text import Text
from .sequence import Sequence


class GameBase:
    def __init__(
        self,
        title: str,
        frame_width: int,
        frame_height: int,
        offset: tuple[int, int, int, int] = (0, 0, 0, 0),
        background_color: str = DEF_COLOR,
        framerate: int = 60,
        icon_path: str = "",
    ):
        """
        게임 클래스

        Args:

        title : 윈도우에 표시된는 제목\n
        frame_width : 게임이 동작하는 level_frame의 너비\n
        frame_height : 게임이 동작하는 level_frame의 너비\n
        offset : level_frame과 윈도우 사이의 간격 (left, top, right, bottom)\n
        background_color : 윈도우의 배경색\n
        framerate : 1초 동안 화면을 갱신하는 빈도 (FPS)\n
        icon_path : 윈도우에 표시되는 icon의 이미지 경로 (png)\n
        """
        pygame.init()

        left_offset, top_offset, right_offset, bottom_offset = offset

        # 시스템
        self.title = self.set_title(title)
        self.screen = pygame.display.set_mode(
            (
                frame_width + left_offset + right_offset,
                frame_height + top_offset + bottom_offset,
            )
        )
        self.clock = pygame.time.Clock()
        self.background = background_color
        self.framerate = framerate

        if icon_path:
            self.icon = pygame.image.load(icon_path)
            pygame.display.set_icon(self.icon)

        self.level = LevelBase(left_offset, top_offset, frame_width, frame_height)

        # 플래그
        self.pause_flag = True
        self.game_over_flag = False
        self.run_flag = True

        # 시퀀스 리스트
        self.operate = Sequence()
        self.transfrom = Sequence()
        self.collide = Sequence()
        self.render = Sequence(self.fill_bg)

    @property
    def events(self):
        """발생한 이벤트"""
        return pygame.event.get()

    def set_title(self, title: str):
        """타이틀을 설정한다."""
        if not title:
            return title

        pygame.display.set_caption(title)
        return title

    def Start(self) -> bool:
        """게임 시작화면"""
        return self.Pause(None, True)

    def Pause(self) -> bool:
        """일시 정지 화면"""

    def Operate(self) -> None:
        """이벤트를 읽어 동작 수행"""
        self.operate.call()

    def Transform(self) -> None:
        """오브젝트를 변형한다."""
        self.transfrom.call()

    def Collide(self) -> None:
        """충돌을 체크한다."""
        self.collide.call()

    def Render(self) -> None:
        """화면에 오브젝트와 배경을 그린다."""
        self.render.call()

    def Update(self) -> None:
        """화면과 시간을 업데이트한다."""
        pygame.display.flip()
        self.clock.tick(self.framerate)

    # 화면 채우기
    def fill_bg(self):
        self.screen.fill(self.background)
        self.level.Render(self.screen)


class LevelBase:
    def __init__(self, left: int, top: int, width: int, height: int):
        self.canvas = pygame.Rect((left, top), (width, height))
        self.size = Point(width, height)
        self.color = BLK_COLOR

    def Render(self, screen=pygame.Surface):
        pygame.draw.rect(screen, self.color, self.canvas, 1)
