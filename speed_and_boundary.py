"""
--------------------------------------------------------
#### 這個檔案負責「滑鼠變速按鈕」跟「撞到賽道邊界」(Q7、Q8)
--------------------------------------------------------
"""

import pygame

GEARS = [("1", 4), ("2", 7), ("3", 10), ("4", 20)]  # (按鈕文字, 最高速度)
DEFAULT_GEAR = 1
BUTTON_SIZE = (50, 40)
BUTTON_GAP = 10
TOP_RIGHT_MARGIN = 20
MESSAGE_FRAMES = 30  # "Crashed!" 訊息要停留幾個 frame


def handle_boundary(car, track_back, state, spawn_x, spawn_y, spawn_angle):
    """
    --------------------------------------------------------
    #### 功能 : 檢查車子是否撞到賽道邊界，撞到的話重置分數/進度跟車子位置
    --------------------------------------------------------
    #### 參數
    - car : 車子物件
    - track_back : 賽道碰撞用的底圖
    - state : GameState 物件(記錄 score / checkpoints_passed / message / message_timer)
    - spawn_x, spawn_y, spawn_angle : 車子重生時的座標跟角度
    --------------------------------------------------------
    #### 回傳值
    - 無(直接修改 state 跟 car)
    --------------------------------------------------------
    """
    """
    --------------------------------------------------------
    Q7. 完成撞到賽道邊界要做的事
    Todo : 呼叫 car.collision(track_back) 檢查車子是不是撞到賽道外。
           如果撞到了：
             1. 把 state.score 設成 0
             2. 把 state.checkpoints_passed 設成 [False, False, False]
             3. 把 state.message 設成 "Crashed!"，state.message_timer 設成 MESSAGE_FRAMES
             4. 呼叫 car.reset(spawn_x, spawn_y, spawn_angle) 讓車子回到起點
    Hint : car.collision(track_back) 會回傳 True 或 False，
           你不需要知道它怎麼判斷撞牆，只要拿它的回傳值寫 if 就好
    --------------------------------------------------------
    """
    # Q7 begin
    if "__fill_in__":  # 檢查車子是不是撞到賽道外
        state.score = "__fill_in__"  # 分數歸零
        "__fill_in__"  # 三個檢查點都重設成沒通過
        state.message, state.message_timer = "Crashed!", MESSAGE_FRAMES  # 顯示撞牆提示，並設定要顯示幾個 frame
        car.reset(spawn_x, spawn_y, spawn_angle)  # 車子回到起點，速度跟角度也重設
        if timer is not None:
            timer.reset()  # 從本次所有圈取最快的更新紀錄，然後重置碼表
    # Q7 end


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
        button_w, button_h = BUTTON_SIZE  # 每個按鈕的寬、高
        right_edge = screen_width - TOP_RIGHT_MARGIN  # 最右邊按鈕的右邊界(螢幕寬度減掉留白)
        left_edge = right_edge - len(GEARS) * button_w - (len(GEARS) - 1) * BUTTON_GAP  # 3 個按鈕靠右排，往左推算出第一個按鈕的左邊界
        self.rects = [
            pygame.Rect(left_edge + i * (button_w + BUTTON_GAP), 20, button_w, button_h)
            for i in range(len(GEARS))
        ]  # 依序往右排出 4 個按鈕的矩形範圍
        self.current_gear = DEFAULT_GEAR  # 預設選中的檔位

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
        for i in range(len(self.rects)):  # 把每個按鈕的編號 0、1、2、3 依序拿出來檢查
            if "__fill_in__":  # 判斷滑鼠是不是點在第 i 個按鈕裡面
                self.current_gear = "__fill_in__"  # 把目前檔位換成第 i 個
                return "__fill_in__"  # 回傳這個檔位對應的最高速度
        return None  # 四個按鈕都沒點到，回傳 None
        # Q8 end

    def draw(self, screen, font):
        for i, rect in enumerate(self.rects):
            selected = i == self.current_gear
            pygame.draw.rect(screen, (255, 220, 0) if selected else (40, 40, 40), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            label_text = font.render(GEARS[i][0], True, (0, 0, 0) if selected else (255, 255, 255))
            screen.blit(label_text, label_text.get_rect(center=rect.center))
