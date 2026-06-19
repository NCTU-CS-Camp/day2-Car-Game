"""
--------------------------------------------------------
#### 這個檔案負責「分數規則」跟「最高分」(Q6、Q7)
--------------------------------------------------------
"""

import math

import pygame

FINISH_RECT = pygame.Rect(60, 428, 135, 26)
# 必須依序踩過 CP1 -> CP2 -> CP3 才算一圈，逆向繞圈會先踩到 CP3，順序不對就不會算
CHECKPOINTS = [
    pygame.Rect(710, 210, 80, 80),
    pygame.Rect(1410, 310, 80, 80),
    pygame.Rect(660, 780, 80, 80),
]
FINISH_LEAVE_DISTANCE = 200  # 要先離終點線這麼遠，這一圈才算「出發」
MESSAGE_FRAMES = 30  # "+1 Lap!" 訊息要停留幾個 frame


class GameState:
    """
    --------------------------------------------------------
    #### 物件 : 整場遊戲共用的狀態，傳給其他檔案的函式讀寫
    --------------------------------------------------------
    #### 屬性
    - score : 目前這次的分數
    - high_score : 這次執行期間的最高分
    - armed : 車子是否已經離終點夠遠，這一圈可以開始計分
    - next_checkpoint : 接下來該踩 CHECKPOINTS 的第幾個(0~3)
    - message / message_timer : 畫面上顯示的提示文字跟剩餘 frame 數
    --------------------------------------------------------
    """

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.armed = False
        self.next_checkpoint = 0
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
    distance_from_finish = math.hypot(
        car.x - FINISH_RECT.centerx, car.y - FINISH_RECT.centery
    )

    """
    --------------------------------------------------------
    Q6. 完成「順向繞完一圈才能加分」的規則
    Todo : 賽道上有 3 個檢查點 CHECKPOINTS = [CP1, CP2, CP3]，車子必須按照
           CP1 -> CP2 -> CP3 的順序依序踩到，最後回到終點才算一圈；
           逆向繞圈會先踩到 CP3，順序不對就不會被記分。
           state.next_checkpoint 記錄「接下來該踩第幾個」(0 代表還沒踩過任何一個，
           3 代表三個都踩過了)。寫出三段判斷(三個獨立的 if，依序寫下來)：
           1. 如果 state.armed 還是 False，而且 distance_from_finish > FINISH_LEAVE_DISTANCE，
              就把 state.armed 設成 True，state.next_checkpoint 設成 0
              (代表車子已經離終點夠遠，這一圈正式出發)
           2. 如果 state.armed 是 True，而且 state.next_checkpoint 還沒到 3，而且車子目前
              的位置在 CHECKPOINTS[state.next_checkpoint] 的範圍內，
              就把 state.next_checkpoint 加 1(代表踩到了「接下來該踩的那個」檢查點)
           3. 如果 state.armed 是 True，而且 state.next_checkpoint 已經等於 3，而且
              on_finish_line 是 True，代表順向繞完一圈：state.score += 1，
              state.armed 設回 False，state.next_checkpoint 設回 0，
              並把 state.message 設成 "+1 Lap!"，state.message_timer 設成 MESSAGE_FRAMES
    Hint : CHECKPOINTS 是一個裝了 3 個 pygame.Rect 的 list，
           用 CHECKPOINTS[state.next_checkpoint] 就可以拿到「現在該踩的那一個」，
           跟判斷滑鼠點到哪個按鈕一樣可以用 .collidepoint(car.x, car.y)
    --------------------------------------------------------
    """
    # Q6 begin
    pass
    # Q6 end


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
    # Q7 end
