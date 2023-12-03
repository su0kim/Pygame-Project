from system.game import Game
from system.config import *
import os


def SnakeGame():
    game = Game(
        TITLE,
        FRAME_WIDTH,
        FRAME_HEIGHT,
        (LEFT_OFFSET, TOP_OFFSET, RIGHT_OFFSET, BOTTOM_OFFSET),
        BACKGROUND_COLOR,
        FRAMERATE,
        ICON,
    )
    # 시작 화면
    while game.Start():
        game.Update()

    # 게임 실행
    while game.run_flag:
        if not (game.GameOver() or game.Pause()):
            game.Process()
            game.Render()
        game.Update()

    # 게임 종료
    game.Quit()


if __name__ == "__main__":
    SnakeGame()
