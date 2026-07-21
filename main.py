"""
--------------------------------------------------------
#### 這是「挖空練習版」的主程式，只負責把所有東西串在一起
--------------------------------------------------------
car.py 裡面的物理引擎(怎麼加速、轉彎、判斷撞牆)都已經寫好了，
你完全不需要知道它裡面怎麼算，只要知道「呼叫哪個函式、給什麼參數」就會動。

題目分散在不同檔案裡，main.py 自己只有 Q1：
- main.py               Q1 : 載入圖片
- controls.py           Q2、Q3 : W/S 加速倒車、J/K 轉向
- score.py              Q4、Q5 : 順向繞圈計分、最高分紀錄
- speed_and_boundary.py Q6、Q7 : 滑鼠變速按鈕、撞到賽道邊界
--------------------------------------------------------
"""

import inspect
from pathlib import Path

import pygame

from car import Car
from controls import handle_movement
from score import CHECKPOINTS, GameState, draw_checkpoints, update_high_score, update_lap_progress
from speed_and_boundary import GearButtons, handle_boundary
from timer import LapTimer

_Q6_DONE = '"__fill_in__"' not in inspect.getsource(LapTimer.lap)

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FPS = 30
SPAWN_X, SPAWN_Y, SPAWN_ANGLE = 120, 480, 180
FILL_IN = "__fill_in__"


def _show_q1_notice():
    """
    Q1 還沒完成時，開一個固定大小(800x600)的全黑視窗。
    按關閉視窗或 ESC 即可結束。
    """
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Car Game")

    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

        screen.fill((0, 0, 0))  # 全黑背景
        pygame.display.flip()
        clock.tick(FPS)

def run():
    """
    # Pygame 啟動 !!!
    """
    # 初始化
    pygame.init()

    """
    --------------------------------------------------------
    Q1. 把底下三個 "__fill_in__" 換成「讀取圖片」的程式
    --------------------------------------------------------
    寫法: pygame.image.load(ASSETS_DIR / "檔名")
        - ASSETS_DIR 是 assets 資料夾的位置(上面已設定好)，
          用斜線 / 接上檔名，就是完整路徑。
        - 檔名要用雙引號 " " 包起來(字串)，例如寫成 "xxx.png"，
          不能寫沒引號的 xxx.png (會被當成變數而出錯)。

    寫法示意(檔名自己填):  img = pygame.image.load(ASSETS_DIR / "圖檔.png")

    三個要讀的檔名:
        - "track_front.png" 賽道前景圖(畫面看到的賽道)
        - "track_back.png"  賽道底圖(判斷有沒有撞牆用)
        - "car.png"         車子圖片
    --------------------------------------------------------
    (變數的 img_ 前綴代表「這個變數存的是影像」)
    --------------------------------------------------------
    """
    # Q1 begin
    img_track_front = pygame.image.load(ASSETS_DIR / "track_front.png")
    img_track_back = pygame.image.load(ASSETS_DIR / "track_back.png")
    img_car = pygame.image.load(ASSETS_DIR / "car.png")
    # Q1 end

    if FILL_IN in (img_track_front, img_track_back, img_car):
        _show_q1_notice()
        pygame.quit()
        return

    # 視窗大小、名稱設定
    screen = pygame.display.set_mode(img_track_front.get_size())
    pygame.display.set_caption("Car Game (W/S Accel, J/K Steer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # 遊戲物件初始化
    car = Car(SPAWN_X, SPAWN_Y, SPAWN_ANGLE)  # 車子
    gear_buttons = GearButtons(screen.get_width())  # 換檔按鈕
    car.set_max_speed(gear_buttons.current_speed())  # 依目前檔位設定最高速
    state = GameState()  # 分數、最高分、訊息等遊戲狀態
    lap_timer = LapTimer()  # 碼表

    # 遊戲畫面更新和遊戲主要邏輯的運作
    running = True
    while running:
        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 關閉視窗
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 滑鼠左鍵
                new_speed = gear_buttons.handle_click(event.pos)  # 判斷是否點到換檔按鈕
                if isinstance(new_speed, (int, float)):  # 點到按鈕會回傳新檔位的最高速，沒點到回傳 None
                    car.set_max_speed(new_speed)  # 切換最高速

        # 鍵盤操控(Q2、Q3:W/S 加速倒車、J/K 轉向)
        keys = pygame.key.get_pressed()
        if not lap_timer.is_running and any(keys):  # 偵測第一個按鍵，啟動碼表
            lap_timer.lap()
        handle_movement(keys, car)
        car.update()  # 依加速度與角度更新車子位置

        # 計分與碰撞邏輯
        # 在這一幀可能讓分數歸零(撞牆)或改變之前，先記錄目前分數有沒有破紀錄
        update_high_score(state)  # Q5:更新最高分紀錄
        score_before = state.score
        checkpoints_before = list(state.checkpoints_passed)
        car_before = (car.x, car.y, car.angle, car.velocity, car.acceleration)
        timer_before = (lap_timer.is_running, lap_timer._lap_start, list(lap_timer._laps))
        handle_boundary(car, img_track_back, state, SPAWN_X, SPAWN_Y, SPAWN_ANGLE, lap_timer)  # Q7:撞到邊界處理
        if not isinstance(state.score, int) or not isinstance(state.checkpoints_passed, list):
            state.score = score_before
            state.checkpoints_passed = checkpoints_before
            car.x, car.y, car.angle, car.velocity, car.acceleration = car_before
            lap_timer.is_running, lap_timer._lap_start, lap_timer._laps = timer_before
        score_before_lap = state.score
        update_lap_progress(car, state)  # Q4:順向繞圈計分
        if state.score > score_before_lap:  # 分數增加 = 通過終點線完成一圈
            try:
                lap_timer.lap()  # Q6 寫完後，這裡會記錄圈速
            except TypeError:
                pass  # Q6 還沒寫完時 lap_time 可能不是數字，先忽略

        # 畫面繪製
        screen.blit(img_track_front, (0, 0))  # 賽道背景
        if state.show_checkpoints:
            draw_checkpoints(screen, font, state)  # 畫出 checkpoint 的位置
        car.draw(screen, img_car)  # 車子

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

        # 碼表顯示
        if _Q6_DONE:
            lap_text = font.render(f"Lap:  {lap_timer.current_lap_str()}", True, (255, 255, 255))
            best_text = font.render(f"Best: {lap_timer.best_lap_str()}", True, (255, 220, 0))
            screen.blit(lap_text, (20, 128))
            screen.blit(best_text, (20, 164))

        # 更新顯示、控制幀率
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
