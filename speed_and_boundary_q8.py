"""
--------------------------------------------------------
#### 這個檔案負責「滑鼠變速按鈕」跟「撞到賽道邊界」(Q8)
--------------------------------------------------------
"""

import pygame

GEARS = [("1", 4), ("2", 7), ("3", 10), ("4", 20)]  # (按鈕文字, 最高速度)
DEFAULT_GEAR = 1
BUTTON_SIZE = (50, 40)
BUTTON_GAP = 10
TOP_RIGHT_MARGIN = 20
MESSAGE_FRAMES = 30  # "Crashed!" 訊息要停留幾個 frame


def handle_boundary(car, track_back, state, spawn_x, spawn_y, spawn_angle, timer=None):
    if car.collision(track_back):
        state.score = 0
        state.checkpoints_passed = [False, False, False]
        state.message, state.message_timer = "Crashed!", MESSAGE_FRAMES
        car.reset(spawn_x, spawn_y, spawn_angle)
        if timer is not None:
            timer.reset()


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
        """
        --------------------------------------------------------
        #### 功能 : 處理滑鼠點擊，判斷有沒有點到變速按鈕
        --------------------------------------------------------
        #### 參數
        - pos : 滑鼠點擊的座標 (x, y)
        --------------------------------------------------------
        #### 回傳值
        - 如果點到按鈕，回傳新檔位的最高速度
        - 如果沒點到任何按鈕，回傳 None
        --------------------------------------------------------
        """
        """
        --------------------------------------------------------
        Q8. 完成滑鼠點擊變速按鈕的判斷
        Todo : 找出滑鼠點到了 self.rects 裡的第幾個按鈕，
               把 self.current_gear 換成那個編號，
               並回傳新的速度(self.current_speed())。
               如果沒有點到任何按鈕，要回傳 None
        Hint : 用 for i in range(len(self.rects)): 把每個按鈕的編號跑一遍
               用 self.rects[i].collidepoint(pos) 判斷滑鼠是不是點在這個按鈕裡面
        --------------------------------------------------------
        """
        # Q8 begin
        for i in range(len(self.rects)):  # 把每個按鈕的編號 0、1、2 依序拿出來檢查
            if "__fill_in__":  # 判斷滑鼠是不是點在第 i 個按鈕裡面
                self.current_gear = "__fill_in__"  # 把目前檔位換成第 i 個
                return "__fill_in__"  # 回傳這個檔位對應的最高速度
        return None  # 三個按鈕都沒點到，回傳 None
        # Q8 end

    def draw(self, screen, font):
        for i, rect in enumerate(self.rects):
            selected = i == self.current_gear
            pygame.draw.rect(screen, (255, 220, 0) if selected else (40, 40, 40), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            label_text = font.render(GEARS[i][0], True, (0, 0, 0) if selected else (255, 255, 255))
            screen.blit(label_text, label_text.get_rect(center=rect.center))
