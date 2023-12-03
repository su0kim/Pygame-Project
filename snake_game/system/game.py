import pygame
from component.level import Level

from framework import *
from system.config import *


class Game:
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

        # 오브젝트
        self.level = Level(left_offset, top_offset, frame_width, frame_height)

        # 폰트
        self.menu_font = pygame.font.SysFont(FONT, FONT_SIZE)
        self.score_font = pygame.font.SysFont(FONT, int(FONT_SIZE * 0.5))

        # 플래그
        self.pause_flag = True
        self.game_over_flag = False
        self.run_flag = True

        self.hard_flag = False
        self.easy_flag = False

        # 난이도
        self.difficulty = 1

    @property
    def events(self):
        """발생한 이벤트"""
        return pygame.event.get()

    @property
    def snake(self):
        return self.level.snake

    @property
    def apple(self):
        return self.level.apple

    @property
    def score(self):
        return len(self.snake.body) - 1

    def set_title(self, title: str):
        """타이틀을 설정한다."""
        if not title:
            return title

        pygame.display.set_caption(title)
        return title

    def appear_setting(self, position, can_edit: bool = False) -> None:
        """설정 창을 띄운다."""
        self.hard_flag = False
        self.easy_flag = False

        L_arrow = Polygon(Point(0, 30), Point(30, 0), Point(30, 60))
        R_arrow = L_arrow.invert()

        if can_edit:
            L_arrow = L_arrow.move_to(position + Point(-100, -100))
            R_arrow = R_arrow.move_to(position + Point(100, -100))

            L_arrow_rect = pygame.draw.polygon(self.screen, BLK_COLOR, L_arrow.coord)
            R_arrow_rect = pygame.draw.polygon(self.screen, BLK_COLOR, R_arrow.coord)

            pygame.draw.polygon(self.screen, DEF_COLOR, L_arrow.coord, 4)
            pygame.draw.polygon(self.screen, DEF_COLOR, R_arrow.coord, 4)

            if Is_MouseOver(L_arrow_rect):
                self.easy_flag = True

            elif Is_MouseOver(R_arrow_rect):
                self.hard_flag = True

        msg = str("난이도")
        text = Text(msg, self.score_font)
        text.Render(self.screen, position + Point(0, -150), EnumAlign.BOTCENTER)

        msg = str(self.difficulty)
        text = Text(msg, self.menu_font)
        text.Render(self.screen, position + Point(0, -110), EnumAlign.MIDDLECENTER)

    def set_difficulty(self) -> None:
        """난이도를 설정한다."""
        if MouseInput(LCLICK) and self.hard_flag:
            self.difficulty += 1

        elif MouseInput(LCLICK) and self.easy_flag:
            self.difficulty -= 1

        self.difficulty = min(self.difficulty, 10)
        self.difficulty = max(self.difficulty, 1)

    def Start(self) -> bool:
        """게임 시작화면"""
        if not self.Pause(None, True):
            return False

        return True

    def Process(self) -> None:
        """event에 따라 연산을 진행한다."""
        self.level.generate_apple()

        # event 확인, Quit event 발생 시 종료.
        for event in self.events:
            if event.type == pygame.QUIT:
                self.run_flag = False

            if event.type == pygame.WINDOWFOCUSLOST:
                self.pause_flag = True

            if event.type == pygame.KEYDOWN:
                direction = self.snake.dir.copy()

                if KeyInput(UP):
                    direction = DIR_UP
                if KeyInput(DOWN):
                    direction = DIR_DOWN
                if KeyInput(LEFT):
                    direction = DIR_LEFT
                if KeyInput(RIGHT):
                    direction = DIR_RIGHT

                self.snake.set_dir(direction)

                if KeyInput(PAUSE):
                    self.pause_flag = True

                if KeyInput(QUIT):
                    self.run_flag = False

        if self.pause_flag:
            return

        # 연산에 따라 오브젝트 이동
        self.snake.move()

        # 이동에 따른 충돌 체크
        self.game_over_flag = self.level.is_conflict()
        self.level.eat_apple()

    def Render(self) -> None:
        """Image들을 렌더링한다."""
        if self.game_over_flag:
            return

        # 배경
        self.screen.fill(self.background)
        self.level.Render(self.screen)

        position = Point(self.level.canvas.left, 10)
        text = Text("pause : Spacebar", self.score_font, BLK_COLOR)
        text.Render(self.screen, position, EnumAlign.TOPLEFT)

        position = position + Point(0, text.size.y * 1.5)
        text = Text("quit : Esc", self.score_font, BLK_COLOR)
        text.Render(self.screen, position, EnumAlign.TOPLEFT)

        # 난이도
        position = Point(self.level.canvas.right, 10)
        text = Text("difficulty : " + str(self.difficulty), self.score_font, BLK_COLOR)
        text.Render(self.screen, position, EnumAlign.TOPRIGHT)

        # 점수
        position = Point(self.screen.get_width() / 2, TOP_OFFSET / 2)
        score = Text(str(self.score), self.score_font, BLK_COLOR)
        score.Render(self.screen, position, EnumAlign.MIDDLECENTER)

        # 오브젝트
        self.snake.Render(self.screen, 1, (128, 128, 128), 20, 0.01)

        if self.apple:
            self.apple.Render(self.screen)

    def Update(self) -> None:
        """화면과 게임 시간을 업데이트한다."""

        # 화면
        pygame.display.flip()

        # 시간
        self.clock.tick(self.framerate + self.score * self.difficulty * 0.1)

    def Pause(
        self, restart_key: int = RESTART, is_start: bool = False, overlay=True
    ) -> bool:
        """게임을 일시정지한다."""
        if not self.pause_flag:
            return False

        # 게임 화면
        self.Render()

        if not overlay:
            return True

        # 흰색 안개
        overlay = self.screen.copy()
        overlay.fill(pygame.Color(255, 255, 255, 100))
        overlay.set_alpha(125)
        self.screen.blit(overlay, (0, 0))

        # 난이도 설정
        position = Point(*self.screen.get_size()) / 2
        self.appear_setting(position, is_start)

        # 텍스트
        msg = MSG_START if is_start else MSG_RESTART
        position = Point(*self.screen.get_size()) / 2  # type: Point
        text = Text(msg, self.menu_font)
        text.Render(self.screen, position, EnumAlign.MIDDLECENTER)

        if self.Restart(restart_key, is_start):
            self.pause_flag = False
            return False

        return True

    def GameOver(self) -> bool:
        """게임 오버"""
        if not self.game_over_flag:
            return False

        self.screen.fill("white")

        position1 = Point(*self.screen.get_size()) / 2 + Point(0, 50)  # type: Point
        text1 = Text(MSG_GAMEOVER, self.menu_font)
        text1.Render(self.screen, position1, EnumAlign.MIDDLECENTER)

        position2 = position1 + Point(0, text1.size.y + 100)
        text2 = Text("score : " + str(self.score), self.score_font)
        text2.Render(self.screen, position2, EnumAlign.TOPCENTER)

        position3 = position1 + Point(0, text1.size.y / 2 + 60)
        text3 = Text(MSG_RESTART, self.score_font)
        text3.Render(self.screen, position3, EnumAlign.TOPCENTER)

        self.appear_setting(position1 + Point(0, -50), True)

        if self.Restart(RESTART, True):
            self.game_over_flag = False
            return False

        return True

    def Restart(self, key: int = RESTART, reset: bool = False) -> None:
        """게임을 다시 시작한다."""
        for event in self.events:
            if event.type == pygame.QUIT:
                self.run_flag = False
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and reset:
                self.set_difficulty()

            if event.type == pygame.KEYDOWN:
                if KeyInput(QUIT):
                    self.run_flag = False
                    return True

                elif KeyInput(key):
                    self.pause_flag = False
                    if reset:
                        self.level = Level(
                            LEFT_OFFSET, TOP_OFFSET, FRAME_WIDTH, FRAME_HEIGHT
                        )
                    return True

        return False

    def Quit(self) -> None:
        """게임을 종료한다."""
        pygame.quit()
