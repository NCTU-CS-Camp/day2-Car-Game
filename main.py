from pathlib import Path

import pygame

from car import ACCEL, ROTATE_SPEED, Car
from race import GearButtons, RaceState

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FPS = 30
SPAWN_X, SPAWN_Y, SPAWN_ANGLE = 120, 480, 180


def run():
    """
    # Pygame 啟動 !!!
    """
    # 初始化
    pygame.init()

    # 圖片素材載入(賽道前景、賽道碰撞層、車子)
    track_front = pygame.image.load(ASSETS_DIR / "track_front.png")
    track_back = pygame.image.load(ASSETS_DIR / "track_back.png")
    car_image = pygame.image.load(ASSETS_DIR / "car.png")

    # 視窗大小、名稱設定
    screen = pygame.display.set_mode(track_front.get_size())
    pygame.display.set_caption("Car Game (W/S Accel, J/K Steer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # 遊戲物件初始化
    car = Car(SPAWN_X, SPAWN_Y, SPAWN_ANGLE)  # 車子
    gear_buttons = GearButtons(screen.get_width())  # 換檔按鈕
    car.set_max_speed(gear_buttons.current_speed())  # 依目前檔位設定最高速
    race = RaceState()  # 計時、圈數等比賽狀態

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

        # 鍵盤操控
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            car.set_accel(ACCEL)  # W:前進加速
        elif keys[pygame.K_s]:
            car.set_accel(-ACCEL)  # S:後退/煞車
        else:
            car.set_accel(0)  # 沒踩油門,靠摩擦力減速
        if keys[pygame.K_j]:
            car.rotate(-ROTATE_SPEED)  # J:左轉
        if keys[pygame.K_k]:
            car.rotate(ROTATE_SPEED)  # K:右轉
        car.update()  # 依加速度與角度更新車子位置

        # 碰撞偵測
        if car.collision(track_back):
            race.handle_crash()  # 記錄撞車
            car.reset(SPAWN_X, SPAWN_Y, SPAWN_ANGLE)  # 車子回到起點

        # 更新比賽狀態(計時、進度等)
        race.update(car)

        # 畫面繪製(由下而上依序疊圖)
        screen.blit(track_front, (0, 0))  # 賽道背景
        car.draw(screen, car_image)  # 車子
        race.draw(screen, font)  # 比賽資訊文字
        gear_buttons.draw(screen, font)  # 換檔按鈕

        # 更新顯示、控制幀率
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
