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
#### 為什麼可以「寫一題就執行看一題」？
--------------------------------------------------------
這個 main.py 採用「安全執行」的方式：
還沒寫完的題目(裡面還留著 "__fill_in__")可能會讓那個檔案出錯，
這裡會自動偵測、把那個還沒完成的功能先「跳過」，而不是讓整個遊戲打不開。
所以你每完成一題，就能直接執行看到那一題的效果，其他沒寫的先擺著沒關係。
你不需要改動這段機制，只要專心把各題的 "__fill_in__" 填好即可。
--------------------------------------------------------
"""

import importlib
from pathlib import Path

import pygame

from car import Car

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FPS = 30
SPAWN_X, SPAWN_Y, SPAWN_ANGLE = 120, 480, 180
FILL_IN = "__fill_in__"  # 還沒填的空格會長這樣


# ===== 安全執行工具：讓「還沒寫完的題目」不會讓整個遊戲掛掉 =====


def _safe(label, func, *args, **kwargs):
    """
    呼叫某個「可能還沒寫完」的函式。
    - 如果這個功能根本還沒載入(func 是 None)：直接跳過。
    - 如果呼叫時出錯(通常是還留著 "__fill_in__")：先跳過。
    等你把那一題寫對了，它就會自然開始運作(過程不會在 terminal 印任何訊息)。
    """
    if func is None:
        return None
    try:
        return func(*args, **kwargs)
    except Exception:
        return None


def _load(module_name):
    """
    嘗試載入某個檔案(模組)。
    如果那個檔案因為還沒填空而有語法錯誤(例如縮排錯誤)，
    這裡會回傳 None，讓相關功能先停用，而不是讓程式直接崩潰。
    """
    try:
        return importlib.import_module(module_name)
    except Exception:
        return None


def _show_q1_notice(track_front, track_back, car_image):
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


class _FallbackGameState:
    """當 score.py 還沒寫完、無法載入時，用這個頂著，讓遊戲先跑起來。"""

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.checkpoints_passed = [False, False, False]
        self.message = ""
        self.message_timer = 0


class _FallbackGearButtons:
    """當 speed_and_boundary.py 還沒寫完、無法載入時的替身按鈕(不顯示也沒關係)。"""

    def __init__(self, screen_width):
        pass

    def current_speed(self):
        return 7  # 預設用第 2 檔的速度

    def handle_click(self, pos):
        return None

    def draw(self, screen, font):
        pass


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

    # Q1 還沒寫完的話，開一個視窗把提示畫出來(而不是只印在 terminal)
    if FILL_IN in (track_front, track_back, car_image):
        _show_q1_notice(track_front, track_back, car_image)
        pygame.quit()
        return

    # 安全載入其他題目所在的檔案(沒寫完的會被自動跳過)
    controls = _load("controls")
    score = _load("score")
    speed_and_boundary = _load("speed_and_boundary")

    handle_movement = getattr(controls, "handle_movement", None)  # Q2、Q3
    update_lap_progress = getattr(score, "update_lap_progress", None)  # Q4
    update_high_score = getattr(score, "update_high_score", None)  # Q5
    GameState = getattr(score, "GameState", _FallbackGameState)
    GearButtons = getattr(speed_and_boundary, "GearButtons", _FallbackGearButtons)  # Q6
    handle_boundary = getattr(speed_and_boundary, "handle_boundary", None)  # Q7

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
                new_speed = _safe("Q6 換檔按鈕", gear_buttons.handle_click, event.pos)
                # 只有在拿到「真的速度數字」時才切換(Q6 沒寫完時會拿到 "__fill_in__")
                if isinstance(new_speed, (int, float)):
                    car.set_max_speed(new_speed)  # 切換最高速

        # 鍵盤操控(Q2、Q3:W/S 加速倒車、J/K 轉向)
        keys = pygame.key.get_pressed()
        _safe("Q2/Q3 鍵盤操控", handle_movement, keys, car)
        car.update()  # 依加速度與角度更新車子位置

        # 計分與碰撞邏輯
        # 在這一幀可能讓分數歸零(撞牆)或改變之前，先記錄目前分數有沒有破紀錄
        _safe("Q5 最高分紀錄", update_high_score, state)
        _safe("Q7 撞牆判定", handle_boundary, car, track_back, state, SPAWN_X, SPAWN_Y, SPAWN_ANGLE)
        _safe("Q4 繞圈計分", update_lap_progress, car, state)

        # 畫面繪製
        screen.blit(track_front, (0, 0))  # 賽道背景
        _safe("車子繪製(Q1 car_image)", car.draw, screen, car_image)  # 車子

        # 分數與訊息文字
        score_text = font.render(f"Score: {state.score}", True, (255, 255, 255))
        high_score_text = font.render(f"Best: {state.high_score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))  # 目前分數
        screen.blit(high_score_text, (20, 56))  # 最高分
        if state.message_timer > 0:  # 有提示訊息時顯示一段時間
            message_text = font.render(state.message, True, (255, 220, 0))
            screen.blit(message_text, (20, 92))
            state.message_timer -= 1  # 倒數計時,時間到就不再顯示

        _safe("Q6 換檔按鈕繪製", gear_buttons.draw, screen, font)  # 換檔按鈕

        # 更新顯示、控制幀率
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
