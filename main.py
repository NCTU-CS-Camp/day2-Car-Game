"""
--------------------------------------------------------
#### 這是「挖空練習版」的主程式，只負責把所有東西串在一起
--------------------------------------------------------
car.py 裡面的物理引擎(怎麼加速、轉彎、判斷撞牆)都已經寫好了，
你完全不需要知道它裡面怎麼算，只要知道「呼叫哪個函式、給什麼參數」就會動。

題目分散在不同檔案裡，main_blank.py 自己只有 Q1：
- main_blank.py               Q1 : 載入圖片
- controls_blank.py           Q2、Q3 : W/S 加速倒車、J/K 轉向
- speed_and_boundary_blank.py Q4、Q5 : 滑鼠變速按鈕、撞到賽道邊界
- score_blank.py              Q6、Q7 : 順向繞圈計分、最高分紀錄

全部寫完之後執行 `python3 main_blank.py`，應該要跟 `main.py` 玩起來一樣。
--------------------------------------------------------
"""

from pathlib import Path

import pygame

from car import Car
from controls import handle_movement
from score import GameState, update_high_score, update_lap_progress
from speed_and_boundary import GearButtons, handle_boundary

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FPS = 30
SPAWN_X, SPAWN_Y, SPAWN_ANGLE = 120, 480, 180


def run():
    """
    # Pygame 啟動 !!!
    """
    # 初始化
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

    # 視窗大小、名稱設定
    screen = pygame.display.set_mode(track_front.get_size())
    pygame.display.set_caption("Car Game (W/S Accel, J/K Steer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # 遊戲物件初始化
    car = Car(SPAWN_X, SPAWN_Y, SPAWN_ANGLE)  # 車子
    gear_buttons = GearButtons(screen.get_width())  # 換檔按鈕
    car.set_max_speed(gear_buttons.current_speed())  # 依目前檔位設定最高速
    state = GameState()  # 分數、最高分、訊息等遊戲狀態

    # 遊戲畫面更新和遊戲主要邏輯的運作
    running = True
    while running:
        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 關閉視窗
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 滑鼠左鍵
                new_speed = gear_buttons.handle_click(event.pos)  # 判斷是否點到換檔按鈕
                if new_speed is not None:
                    car.set_max_speed(new_speed)  # 切換最高速

        # 鍵盤操控(Q2、Q3:W/S 加速倒車、J/K 轉向)
        keys = pygame.key.get_pressed()
        handle_movement(keys, car)
        car.update()  # 依加速度與角度更新車子位置

        # 計分與碰撞邏輯
        # 在這一幀可能讓分數歸零(撞牆)或改變之前，先記錄目前分數有沒有破紀錄
        update_high_score(state)  # Q7:更新最高分紀錄
        handle_boundary(car, track_back, state, SPAWN_X, SPAWN_Y, SPAWN_ANGLE)  # Q5:撞到邊界處理
        update_lap_progress(car, state)  # Q6:順向繞圈計分

        # 畫面繪製
        screen.blit(track_front, (0, 0))  # 賽道背景
        car.draw(screen, car_image)  # 車子

        # 分數與訊息文字
        score_text = font.render(f"Score: {state.score}", True, (255, 255, 255))
        high_score_text = font.render(f"Best: {state.high_score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))  # 目前分數
        screen.blit(high_score_text, (20, 56))  # 最高分
        if state.message_timer > 0:  # 有提示訊息時顯示一段時間
            message_text = font.render(state.message, True, (255, 220, 0))
            screen.blit(message_text, (20, 92))
            state.message_timer -= 1  # 倒數計時,時間到就不再顯示

        gear_buttons.draw(screen, font)  # 換檔按鈕

        # 更新顯示、控制幀率
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
