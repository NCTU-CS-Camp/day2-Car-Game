"""
--------------------------------------------------------
#### 這個檔案負責「分數規則」跟「最高分」(Q6、Q7)
--------------------------------------------------------
"""

import pygame

FINISH_RECT = pygame.Rect(60, 428, 135, 26)
# 必須依序踩過 CP1 -> CP2 -> CP3 才算一圈，逆向繞圈會先踩到 CP3，順序不對就不會算
CHECKPOINTS = [
    pygame.Rect(710, 210, 80, 80),
    pygame.Rect(1410, 310, 80, 80),
    pygame.Rect(660, 780, 80, 80),
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
    - checkpoints_passed : CP1、CP2、CP3 是否已依序通過
    - message / message_timer : 畫面上顯示的提示文字跟剩餘 frame 數
    --------------------------------------------------------
    """

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.checkpoints_passed = [False, False, False]
        self.message = ""
        self.message_timer = 0


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
    Q6-1. 處理車子通過 CP1
    Todo : 如果車子位於 CP1：
           1. CP2 已通過時，代表車子從 CP2 逆向回到 CP1，
              將 CP2 改為尚未通過。
           2. 否則，只有三個 checkpoint 都尚未通過時，
              才把 CP1 設為已通過。
    Hint : 
           1. CP1、CP2 分別是 state.checkpoints_passed[0]、[1]。
           2. 可以用 any(state.checkpoints_passed) 來判斷是否已有任一 checkpoint 通過。
    --------------------------------------------------------
    """
    # Q6-1 begin
    if on_checkpoint_1:
        if "__fill_in__":
            state.checkpoints_passed[1] = False
        elif "__fill_in__":
            state.checkpoints_passed[0] = True
    # Q6-1 end

    # Q6-1 answer:
    # if on_checkpoint_1:
    #     if state.checkpoints_passed[1]:
    #         state.checkpoints_passed[1] = False
    #     elif not any(state.checkpoints_passed):
    #         state.checkpoints_passed[0] = True

    """
    --------------------------------------------------------
    Q6-2. 處理車子通過 CP2
    Todo : 如果車子位於 CP2：
           1. CP3 已通過時，代表車子從 CP3 逆向回到 CP2，
              將 CP3 改為尚未通過。
           2. 否則，只有 CP1 已通過且 CP2 尚未通過時，
              才把 CP2 設為已通過。
    Hint : 
           1. CP1、CP2、CP3 分別是 state.checkpoints_passed[0]、[1]、[2]。
           2. 
    --------------------------------------------------------
    """
    # Q6-2 begin
    if on_checkpoint_2:
        if "__fill_in__":
            state.checkpoints_passed[2] = False
        elif "__fill_in__" and "__fill_in__":
            state.checkpoints_passed[1] = True
    # Q6-2 end

    # Q6-2 answer:
    # if on_checkpoint_2:
    #     if state.checkpoints_passed[2]:
    #         state.checkpoints_passed[2] = False
    #     elif state.checkpoints_passed[0] and not state.checkpoints_passed[1]:
    #         state.checkpoints_passed[1] = True

    """
    --------------------------------------------------------
    Q6-3. 處理車子通過 CP3
    Todo : 車子位於 CP3，而且 CP2 已通過、CP3 尚未通過時，
           將 CP3 設為已通過。
    Hint : 
           1. CP2、CP3 分別是 state.checkpoints_passed[1]、[2]。
    --------------------------------------------------------
    """
    # Q6-3 begin
    if (
        on_checkpoint_3
        and "__fill_in__"
        and "__fill_in__"
    ):
        state.checkpoints_passed[2] = True
    # Q6-3 end

    # Q6-3 answer:
    # if (
    #     on_checkpoint_3
    #     and state.checkpoints_passed[1]
    #     and not state.checkpoints_passed[2]
    # ):
    #     state.checkpoints_passed[2] = True

    """
    --------------------------------------------------------
    Q6-4. 處理車子完成一圈
    Todo : 車子位於終點，而且 CP3 已通過時：
           1. 將 state.score 加 1。
           2. 將三個 checkpoint 全部重設為尚未通過。
           3. 將 state.message 設成 "+1 Lap!"。
           4. 將 state.message_timer 設成 MESSAGE_FRAMES。
    Hint : 使用 on_finish_line 和 state.checkpoints_passed[2] 判斷。
           可以用 for 迴圈重設所有 checkpoint。
           例如 state.checkpoints_passed[0] = False 可將 CP1 設為尚未通過。
    --------------------------------------------------------
    """
    # Q6-4 begin
    if on_finish_line and "__fill_in__":
        state.score += 1
        for i in range(3):
            "__fill_in__"
        state.message = "+1 Lap!"
        state.message_timer = MESSAGE_FRAMES
    # Q6-4 end

    # Q6-4 answer:
    # if on_finish_line and "__fill_in__":
    #     state.score += 1
    #     for i in range(3):
    #         state.checkpoints_passed[i] = False
    #     state.message = "+1 Lap!"
    #     state.message_timer = MESSAGE_FRAMES


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
    Q7. 完成最高分的紀錄
    Todo : 如果 state.score 超過 state.high_score，就把 state.high_score 更新成 state.score
    Hint : 單純的數字比較，if state.score > state.high_score: ...
    --------------------------------------------------------
    """
    # Q7 begin
    pass
    # 參考答案：
    # if state.score > state.high_score:
    #     state.high_score = state.score
    # Q7 end
