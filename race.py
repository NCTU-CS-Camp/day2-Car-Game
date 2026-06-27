"""
--------------------------------------------------------
#### 這個檔案放「比賽規則」跟「變速按鈕」，把 main.py 不需要知道的細節包起來
--------------------------------------------------------
"""

import pygame

FINISH_RECT = pygame.Rect(50, 420, 145, 35)
# 必須依序踩過 CP1 -> CP2 -> CP3 才算一圈，逆向繞圈會先踩到 CP3，順序不對就不會算
CHECKPOINTS = [
    pygame.Rect(740, 175, 30, 160),
    pygame.Rect(1395, 335, 160, 30),
    pygame.Rect(790, 710, 30, 155),
]
MESSAGE_FRAMES = 30  # "+1 Lap!" / "Crashed!" 訊息要停留幾個 frame

GEARS = [("1", 4), ("2", 7), ("3", 10)]  # (按鈕文字, 最高速度)
DEFAULT_GEAR = 1
BUTTON_SIZE = (50, 40)
BUTTON_GAP = 10
TOP_RIGHT_MARGIN = 20


class RaceState:
    """
    --------------------------------------------------------
    #### 物件 : 比賽規則(終點線、檢查點、分數、最高分、提示訊息)
    --------------------------------------------------------
    #### 函式
    - update(car) : 每一幀呼叫一次，檢查車子有沒有順向繞完一圈
    - handle_crash() : 車子撞牆時呼叫，分數歸零、進度重設
    - draw(screen, font) : 把 Score / Best / 提示訊息畫到畫面上
    --------------------------------------------------------
    #### 屬性
    - score : 目前這次的分數
    - high_score : 這次執行期間的最高分
    - checkpoints_passed : CP1、CP2、CP3 是否已依序通過
    --------------------------------------------------------
    """

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.checkpoints_passed = [False, False, False]
        self.message = ""
        self.message_timer = 0

    def _register_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def handle_crash(self):
        self._register_high_score()
        self.score = 0
        for i in range(3):
            self.checkpoints_passed[i] = False
        self.message, self.message_timer = "Crashed!", MESSAGE_FRAMES

    def update(self, car):
        on_finish_line = FINISH_RECT.collidepoint(car.x, car.y)
        on_checkpoint_1 = CHECKPOINTS[0].collidepoint(car.x, car.y)
        on_checkpoint_2 = CHECKPOINTS[1].collidepoint(car.x, car.y)
        on_checkpoint_3 = CHECKPOINTS[2].collidepoint(car.x, car.y)

        # if on_checkpoint_1:
        #     if self.checkpoints_passed[1]:
        #         self.checkpoints_passed[1] = False
        #     elif not any(self.checkpoints_passed):
        #         self.checkpoints_passed[0] = True

        # if on_checkpoint_2:
        #     if self.checkpoints_passed[2]:
        #         self.checkpoints_passed[2] = False
        #     elif self.checkpoints_passed[0] and not self.checkpoints_passed[1]:
        #         self.checkpoints_passed[1] = True

        # if (
        #     on_checkpoint_3
        #     and self.checkpoints_passed[1]
        #     and not self.checkpoints_passed[2]
        # ):
        #     self.checkpoints_passed[2] = True

        # if on_finish_line and self.checkpoints_passed[2]:
        #     self.score += 1
        #     self._register_high_score()
        #     for i in range(3):
        #         self.checkpoints_passed[i] = False
        #     self.message, self.message_timer = "+1 Lap!", MESSAGE_FRAMES


        if on_checkpoint_1:
            self.checkpoints_passed[0] = True
            if self.checkpoints_passed[1]:
                self.checkpoints_passed[1] = False
        if on_checkpoint_2:
            if self.checkpoints_passed[2]:
                self.checkpoints_passed[2] = False
            elif self.checkpoints_passed[0]:
                self.checkpoints_passed[1] = True
        if on_checkpoint_3:
            if not self.checkpoints_passed[1]:
                self.checkpoints_passed[2] = False
            else:
                self.checkpoints_passed[2] = True

        if on_finish_line:
            if all(self.checkpoints_passed):
                self.score += 1
                self.message = "+1 Lap!"
                self.message_timer = MESSAGE_FRAMES
            for i in range(3):
                self.checkpoints_passed[i] = False

    def draw(self, screen, font):
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = font.render(f"Best: {self.high_score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (20, 56))
        if self.message_timer > 0:
            message_text = font.render(self.message, True, (255, 220, 0))
            screen.blit(message_text, (20, 92))
            self.message_timer -= 1


class GearButtons:
    """
    --------------------------------------------------------
    #### 物件 : 右上角的三檔變速按鈕
    --------------------------------------------------------
    #### 函式
    - current_speed() : 回傳目前檔位的最高速度
    - handle_click(pos) : 滑鼠點擊時呼叫，回傳新檔位的最高速度(沒點到按鈕回傳 None)
    - draw(screen, font) : 把三個按鈕畫到畫面上
    --------------------------------------------------------
    """

    def __init__(self, screen_width):
        button_w, button_h = BUTTON_SIZE
        right_edge = screen_width - TOP_RIGHT_MARGIN
        left_edge = right_edge - len(GEARS) * button_w - (len(GEARS) - 1) * BUTTON_GAP
        self.rects = [
            pygame.Rect(left_edge + i * (button_w + BUTTON_GAP), 20, button_w, button_h)
            for i in range(len(GEARS))
        ]
        self.current_gear = DEFAULT_GEAR

    def current_speed(self):
        return GEARS[self.current_gear][1]

    def handle_click(self, pos):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                self.current_gear = i
                return self.current_speed()
        return None

    def draw(self, screen, font):
        for i, rect in enumerate(self.rects):
            selected = i == self.current_gear
            pygame.draw.rect(screen, (255, 220, 0) if selected else (40, 40, 40), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            label_text = font.render(GEARS[i][0], True, (0, 0, 0) if selected else (255, 255, 255))
            screen.blit(label_text, label_text.get_rect(center=rect.center))
