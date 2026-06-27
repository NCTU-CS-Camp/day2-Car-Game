"""
--------------------------------------------------------
#### 這個檔案負責「分數規則」跟「最高分」(Q6、Q7)
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
    --------------------------------------------------------
    """

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.message = ""
        self.message_timer = 0
        self.checkpoints_passed = [False, False, False]


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


    skip_Q4_1 = False  # 如果你想先跳過 Q4-1 的部分，請把這個變數改成 True

    if not skip_Q4_1:
        """
        --------------------------------------------------------
        Q4-1. 通過 checkpoint 及 finish line
        Todo : 
            1. 分別判斷車車通過3個檢查點的情況，並依照順序將其設為已通過
            2. 通過終點後，將三個檢查點重設為尚未通過
        Hint : 
            1. 使用 if 判斷式進行判斷
            2. 使用 for 迴圈重設所有 checkpoint
        --------------------------------------------------------
        """
        # Q4-1 begin
        if on_checkpoint_1:
            state.checkpoints_passed[0] = True
        if "__fill_in__":    # 位於 CP2 時，將 CP2 設為已通過
            "__fill_in__"
        if "__fill_in__":    # 位於 CP3 時，將 CP3 設為已通過
            "__fill_in__"

        if "__fill_in__":    # 位於終點時，將三個 checkpoint 重設為尚未通過並加分
            state.score += 1
            state.message = "+1 Lap!"
            state.message_timer = MESSAGE_FRAMES
            "__fill_in__"    # for 迴圈重設所有 checkpoint
                "__fill_in__"
        # Q4-1 end
    else:
        """
        --------------------------------------------------------
        Q4-2. 處理車子通過 finish line
        Todo : 
               !!! 重要 !!! 
               把skip_Q4_1改成True，先跳過 Q4-1 的部分，完成這個接下來的部分
               判斷車車是否為順向通過終點，若是的話就加分
        Hint : all(state.checkpoints_passed) 可以判斷三個 checkpoint 是否都已通過
        --------------------------------------------------------
        """
        # Q4-2 begin
        if on_finish_line:
            if "__fill_in__":    # 如果三個 checkpoint 都已通過，表示順向通過終點
                state.score += 1
                state.message = "+1 Lap!"
                state.message_timer = MESSAGE_FRAMES
            for i in range(3):
                state.checkpoints_passed[i] = False
        # Q4-2 end

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
            if "__fill_in__":    # 如果 CP2 尚未通過，將 CP3 設為尚未通過
                state.checkpoints_passed[2] = False
            else:                # 否則設為通過
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
    pass
    # Q5 end
