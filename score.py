"""
--------------------------------------------------------
#### 這個檔案負責「分數規則」跟「最高分」(Q4、Q5)
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
MESSAGE_FRAMES = 30  # "+1 Lap!" 訊息要停留幾個 frame


class GameState:
    """
    --------------------------------------------------------
    #### 物件 : 整場遊戲共用的狀態，傳給其他檔案的函式讀寫
    --------------------------------------------------------
    #### 屬性
    - score : 目前這次的分數
    - high_score : 這次執行期間的最高分
    - message / message_timer : 畫面上顯示的提示文字跟剩餘 frame 數
    - checkpoints_passed : CP1、CP2、CP3 是否已依序通過
    - show_checkpoints : 是否要在畫面上顯示 checkpoint 的位置
    --------------------------------------------------------
    """

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.message = ""
        self.message_timer = 0
        self.checkpoints_passed = [False, False, False]
        self.show_checkpoints = False  # 是否要在畫面上顯示 checkpoint 的位置

def draw_checkpoints(screen, font, state):
    """
    --------------------------------------------------------
    #### 功能 : 在畫面上畫出 checkpoint 的位置，並顯示是否已通過
    --------------------------------------------------------
    #### 參數
    - screen : pygame 的畫面物件
    - font : pygame 的字型物件
    - state : GameState 物件
    --------------------------------------------------------
    #### 回傳值
    - 無(直接修改 state)
    --------------------------------------------------------
    """
    for i, checkpoint in enumerate(CHECKPOINTS):
        passed = state.checkpoints_passed[i]
        color = (0, 220, 0) if passed else (255, 80, 80)

        pygame.draw.rect(screen, color, checkpoint, 4)

        status = "T" if passed else "F"
        text = font.render(f"CP{i + 1}: {status}", True, color)
        text_rect = text.get_rect(center=checkpoint.center)
        background_rect = text_rect.inflate(12, 6)
        pygame.draw.rect(screen, (0, 0, 0), background_rect)
        screen.blit(text, text_rect)


def update_lap_progress(car, state):
    """
    --------------------------------------------------------
    #### 功能 : 檢查車子有沒有順向繞完一圈，是的話加分
    --------------------------------------------------------
    #### 參數
    - car : 車子物件
    - state : GameState 物件
    --------------------------------------------------------
    #### 回傳值
    - 無(直接修改 state)
    --------------------------------------------------------
    """
    on_finish_line = FINISH_RECT.collidepoint(car.x, car.y)
    on_checkpoint_1 = CHECKPOINTS[0].collidepoint(car.x, car.y)
    on_checkpoint_2 = CHECKPOINTS[1].collidepoint(car.x, car.y)
    on_checkpoint_3 = CHECKPOINTS[2].collidepoint(car.x, car.y)

    """
    --------------------------------------------------------
    Q4-1. 通過 checkpoint
    Todo : 
        1. 顯示 checkpoint 的位置，方便測試
        2. 分別判斷車車通過3個檢查點的情況，並依照順序將其設為已通過
    Hint : 
        1. show_checkpoints 可以控制是否要畫出 checkpoint
        2. state.checkpoints_passed[0] 表示 CP1 是否已通過
    --------------------------------------------------------
    """
    # Q4-1 begin
    "__fill_in__"  # 在地圖上顯示 checkpoint 的位置，方便測試
    if on_checkpoint_1:
        "__fill_in__"
    if on_checkpoint_2:
        "__fill_in__"
    if on_checkpoint_3:
        "__fill_in__"
    # Q4-1 end

    enable_Q4_3 = False  # 如果你想 ... 的部分，請把這個變數改成 True

    if not enable_Q4_3:
        """
        --------------------------------------------------------
        Q4-2. 通過 finish line
        Todo :通過終點後，分數增加，並將三個檢查點重設為尚未通過
        Hint : 
            1. state.score 表示目前分數
            2. 使用 for 迴圈重設所有 checkpoint
        --------------------------------------------------------
        """
        # Q4-2 begin
        if on_finish_line:
            "__fill_in__"
            state.message = "+1 Lap!"
            state.message_timer = MESSAGE_FRAMES
            # TODO : 將三個檢查點重設為尚未通過

        # Q4-2 end

    else:
        """
        --------------------------------------------------------
        Q4-3. 處理車子通過 finish line
        Todo : 
               !!! 重要 !!! 
               先把enable_Q4_3改成True，先跳過 Q4-1 的部分，完成這個接下來的部分
               判斷車車是否為順向通過終點，若是的話就加分
        Hint : all(state.checkpoints_passed) 可以判斷三個 checkpoint 是否都已通過
        --------------------------------------------------------
        """
        # Q4-3 begin
        if on_finish_line:
            if "__fill_in__":
                state.score += 1
                state.message = "+1 Lap!"
                state.message_timer = MESSAGE_FRAMES
            for i in range(3):
                state.checkpoints_passed[i] = False
        # Q4-3 end

        """
        --------------------------------------------------------
        Q4-3. 處理逆向問題
        Todo : 根據 "__fill_in__" 的提示，完成逆向通過 checkpoint 的判斷
        --------------------------------------------------------
        """
        # Q4-3 begin
        if on_checkpoint_1:
            state.checkpoints_passed[0] = True
            if state.checkpoints_passed[1]:
                state.checkpoints_passed[1] = False

        if on_checkpoint_2:
            if "__fill_in__":    # 如果 CP3 已通過，將 CP3 設為尚未通過
                state.checkpoints_passed[2] = False
            elif "__fill_in__":  # 如果 CP1 已通過，將 CP2 設為已通過
                state.checkpoints_passed[1] = True

        if on_checkpoint_3:
            if "__fill_in__":    # 如果 CP2 已通過，將 CP3 設為已通過
                state.checkpoints_passed[2] = True
        
        # Q4-3 end

def update_high_score(state):
    """
    --------------------------------------------------------
    #### 功能 : 如果這次的分數破紀錄，更新最高分
    --------------------------------------------------------
    #### 參數
    - state : GameState 物件
    --------------------------------------------------------
    #### 回傳值
    - 無(直接修改 state.high_score)
    --------------------------------------------------------
    """
    """
    --------------------------------------------------------
    Q5. 完成最高分的紀錄
    Todo : 如果 state.score 超過 state.high_score，就把 state.high_score 更新成 state.score
    Hint : 單純的數字比較，if state.score > state.high_score: ...
    --------------------------------------------------------
    """
    # Q5 begin
    # TODO : 如果這次的分數破紀錄，更新最高分
    
    # Q5 end
