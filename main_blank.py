"""
--------------------------------------------------------
#### 這是「挖空練習版」的主程式
--------------------------------------------------------
car.py 裡面的物理引擎(怎麼加速、轉彎、判斷撞牆)都已經寫好了，
你完全不需要知道它裡面怎麼算，只要知道「呼叫哪個函式、給什麼參數」就會動。

底下總共有 7 個題目要完成(用 Ctrl+F 找 "Q1" ~ "Q7")：
- Q1 : 載入圖片
- Q2 : W / S 加速、倒車
- Q3 : J / K 轉向
- Q4 : 滑鼠點擊變速按鈕
- Q5 : 撞到賽道邊界要做的事
- Q6 : 分數機制(一定要順向繞完一圈才能加分)
- Q7 : 最高分紀錄

全部寫完之後執行 `python3 main_blank.py`，應該要跟 `main.py` 玩起來一樣。
--------------------------------------------------------
"""

import math
from pathlib import Path

import pygame

from car import ACCEL, ROTATE_SPEED, Car

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FPS = 30
SPAWN_X, SPAWN_Y, SPAWN_ANGLE = 120, 480, 180

FINISH_RECT = pygame.Rect(60, 428, 135, 26)
# 必須按照 CP1 -> CP2 -> CP3 的順序依序踩過，逆向繞圈會先踩到 CP3，順序不對就不會算
CHECKPOINTS = [
    pygame.Rect(710, 210, 80, 80),
    pygame.Rect(1410, 310, 80, 80),
    pygame.Rect(660, 780, 80, 80),
]
FINISH_LEAVE_DISTANCE = 200  # 要先離終點線這麼遠，這一圈才算「出發」
MESSAGE_FRAMES = FPS  # "+1 Lap!" / "Crashed!" 訊息要停留幾個 frame

GEARS = [("1", 4), ("2", 7), ("3", 10)]  # (按鈕文字, 最高速度)
DEFAULT_GEAR = 1
GEAR_BUTTON_SIZE = (50, 40)
GEAR_BUTTON_GAP = 10
GEAR_BUTTON_TOP_RIGHT_MARGIN = 20


def run():
    pygame.init()

    """
    --------------------------------------------------------
    Q1. 把底下三個 "__fill_in__" 換成讀取圖片的程式
    Todo : 讀取車子圖片、賽道前景圖、賽道底圖(碰撞用)
    Hint : 用 pygame.image.load(路徑)
           路徑可以用 ASSETS_DIR / "檔名" 組出來
           三個檔名分別是 "track_front.png"、"track_back.png"、"car.png"
    --------------------------------------------------------
    """
    # Q1 begin
    track_front = "__fill_in__"
    track_back = "__fill_in__"
    car_image = "__fill_in__"
    # Q1 end

    screen = pygame.display.set_mode(track_front.get_size())
    pygame.display.set_caption("Car Game (W/S Accel, J/K Steer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    screen_width, _ = track_front.get_size()
    button_w, button_h = GEAR_BUTTON_SIZE
    buttons_right_edge = screen_width - GEAR_BUTTON_TOP_RIGHT_MARGIN
    buttons_left_edge = buttons_right_edge - len(GEARS) * button_w - (len(GEARS) - 1) * GEAR_BUTTON_GAP
    gear_buttons = [
        pygame.Rect(buttons_left_edge + i * (button_w + GEAR_BUTTON_GAP), 20, button_w, button_h)
        for i in range(len(GEARS))
    ]

    car = Car(SPAWN_X, SPAWN_Y, SPAWN_ANGLE)
    current_gear = DEFAULT_GEAR
    car.set_max_speed(GEARS[current_gear][1])

    score = 0
    high_score = 0  # 每次重新執行都會歸零
    armed = False  # 車子是否已經離開終點線，這一圈可以開始計分了
    next_checkpoint = 0  # 接下來該踩 CHECKPOINTS 裡的第幾個(0~3，3 代表三個都踩過了)
    message = ""
    message_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                """
                --------------------------------------------------------
                Q4. 完成滑鼠點擊變速按鈕的判斷
                Todo : 找出滑鼠點到了 gear_buttons 裡的第幾個按鈕，
                       把 current_gear 換成那個編號，
                       並呼叫 car.set_max_speed(...) 換成對應的速度
                Hint : gear_buttons 是一個 list，裡面每個元素是一個 pygame.Rect
                       用 for i, rect in enumerate(gear_buttons): 把每個按鈕跑一遍
                       用 rect.collidepoint(event.pos) 判斷滑鼠是不是點在這個按鈕裡面
                       按鈕 i 對應的速度是 GEARS[i][1]
                --------------------------------------------------------
                """
                # Q4 begin
                pass
                # Q4 end

        keys = pygame.key.get_pressed()

        """
        --------------------------------------------------------
        Q2. 完成 W、S 加速/倒車的判斷
        Todo : 按 W 呼叫 car.set_accel(ACCEL) 加速
               按 S 呼叫 car.set_accel(-ACCEL) 倒車
               兩個都沒按，呼叫 car.set_accel(0)
        Hint : 用 if / elif / else，三種情況只會發生一種
        --------------------------------------------------------
        """
        # Q2 begin
        pass
        # Q2 end

        """
        --------------------------------------------------------
        Q3. 完成 J、K 轉向的判斷
        Todo : 按 J 呼叫 car.rotate(-ROTATE_SPEED) 左轉
               按 K 呼叫 car.rotate(ROTATE_SPEED) 右轉
        Hint : 用兩個獨立的 if(不要用 elif)，因為两個鍵理論上互不影響
        --------------------------------------------------------
        """
        # Q3 begin
        pass
        # Q3 end

        car.update()

        """
        --------------------------------------------------------
        Q5. 完成撞到賽道邊界要做的事
        Todo : 呼叫 car.collision(track_back) 檢查車子是不是撞到賽道外。
               如果撞到了：
                 1. 把 score 設成 0
                 2. 把 armed 設成 False，next_checkpoint 設成 0
                 3. 把 message 設成 "Crashed!"，message_timer 設成 MESSAGE_FRAMES
                 4. 呼叫 car.reset(SPAWN_X, SPAWN_Y, SPAWN_ANGLE) 讓車子回到起點
        Hint : car.collision(track_back) 會回傳 True 或 False，
               你不需要知道它怎麼判斷撞牆，只要拿它的回傳值寫 if 就好
        --------------------------------------------------------
        """
        # Q5 begin
        pass
        # Q5 end

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
               next_checkpoint 記錄「接下來該踩第幾個」(0 代表還沒踩過任何一個，
               3 代表三個都踩過了)。寫出三段判斷(三個獨立的 if，依序寫下來)：
               1. 如果還沒 armed，而且 distance_from_finish > FINISH_LEAVE_DISTANCE，
                  就把 armed 設成 True，next_checkpoint 設成 0
                  (代表車子已經離終點夠遠，這一圈正式出發)
               2. 如果 armed 是 True，而且 next_checkpoint 還沒到 3，而且車子目前的位置
                  在 CHECKPOINTS[next_checkpoint] 的範圍內，就把 next_checkpoint 加 1
                  (代表踩到了「接下來該踩的那個」檢查點)
               3. 如果 armed 是 True，而且 next_checkpoint 已經等於 3，而且 on_finish_line
                  是 True，代表順向繞完一圈：score += 1，armed 設回 False，
                  next_checkpoint 設回 0，並把 message 設成 "+1 Lap!"，
                  message_timer 設成 MESSAGE_FRAMES
        Hint : CHECKPOINTS 是一個裝了 3 個 pygame.Rect 的 list，
               用 CHECKPOINTS[next_checkpoint] 就可以拿到「現在該踩的那一個」，
               跟判斷滑鼠點到哪個按鈕一樣可以用 .collidepoint(car.x, car.y)
        --------------------------------------------------------
        """
        # Q6 begin
        pass
        # Q6 end

        """
        --------------------------------------------------------
        Q7. 完成最高分的紀錄
        Todo : 如果這次的 score 超過目前的 high_score，就把 high_score 更新成 score
        Hint : 單純的數字比較，if score > high_score: ...
        --------------------------------------------------------
        """
        # Q7 begin
        pass
        # Q7 end

        screen.blit(track_front, (0, 0))
        car.draw(screen, car_image)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"Best: {high_score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (20, 56))
        if message_timer > 0:
            message_text = font.render(message, True, (255, 220, 0))
            screen.blit(message_text, (20, 92))
            message_timer -= 1

        for i, rect in enumerate(gear_buttons):
            selected = i == current_gear
            pygame.draw.rect(screen, (255, 220, 0) if selected else (40, 40, 40), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            label_text = font.render(GEARS[i][0], True, (0, 0, 0) if selected else (255, 255, 255))
            screen.blit(label_text, label_text.get_rect(center=rect.center))

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
