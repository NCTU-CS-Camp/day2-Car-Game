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
from controls_blank import handle_movement
from score_blank import GameState, update_high_score, update_lap_progress
from speed_and_boundary_blank import GearButtons, handle_boundary

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FPS = 30
SPAWN_X, SPAWN_Y, SPAWN_ANGLE = 120, 480, 180


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
    # 參考答案：
    # track_front = pygame.image.load(ASSETS_DIR / "track_front.png")
    # track_back = pygame.image.load(ASSETS_DIR / "track_back.png")
    # car_image = pygame.image.load(ASSETS_DIR / "car.png")
    # Q1 end

    screen = pygame.display.set_mode(track_front.get_size())
    pygame.display.set_caption("Car Game (W/S Accel, J/K Steer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    car = Car(SPAWN_X, SPAWN_Y, SPAWN_ANGLE)
    gear_buttons = GearButtons(screen.get_width())
    car.set_max_speed(gear_buttons.current_speed())
    state = GameState()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                new_speed = gear_buttons.handle_click(event.pos)
                if new_speed is not None:
                    car.set_max_speed(new_speed)

        keys = pygame.key.get_pressed()
        handle_movement(keys, car)
        car.update()

        # 在這一幀可能讓分數歸零(撞牆)或改變之前，先記錄目前分數有沒有破紀錄
        update_high_score(state)
        handle_boundary(car, track_back, state, SPAWN_X, SPAWN_Y, SPAWN_ANGLE)
        update_lap_progress(car, state)

        screen.blit(track_front, (0, 0))
        car.draw(screen, car_image)

        score_text = font.render(f"Score: {state.score}", True, (255, 255, 255))
        high_score_text = font.render(f"Best: {state.high_score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (20, 56))
        if state.message_timer > 0:
            message_text = font.render(state.message, True, (255, 220, 0))
            screen.blit(message_text, (20, 92))
            state.message_timer -= 1

        gear_buttons.draw(screen, font)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
