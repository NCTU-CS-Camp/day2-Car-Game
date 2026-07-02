"""
--------------------------------------------------------
#### Q1 ~ Q7 已完成，這個版本只剩 Q8 需要填寫
--------------------------------------------------------
- speed_and_boundary_q8.py  Q8 : 滑鼠變速按鈕

全部寫完之後執行 `python3 main_q8.py`，應該要跟 `main.py` 玩起來一樣。
--------------------------------------------------------
"""

from pathlib import Path

import pygame

from car import Car
from controls_done import handle_movement
from score_done import GameState, update_high_score, update_lap_progress
from speed_and_boundary_q8 import GearButtons, handle_boundary
from timer_done import LapTimer

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FPS = 30
SPAWN_X, SPAWN_Y, SPAWN_ANGLE = 120, 480, 180


def run():
    pygame.init()

    track_front = pygame.image.load(ASSETS_DIR / "track_front.png")
    track_back = pygame.image.load(ASSETS_DIR / "track_back.png")
    car_image = pygame.image.load(ASSETS_DIR / "car.png")

    screen = pygame.display.set_mode(track_front.get_size())
    pygame.display.set_caption("Car Game (W/S Accel, J/K Steer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    car = Car(SPAWN_X, SPAWN_Y, SPAWN_ANGLE)
    gear_buttons = GearButtons(screen.get_width())
    car.set_max_speed(gear_buttons.current_speed())
    state = GameState()
    lap_timer = LapTimer()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                new_speed = gear_buttons.handle_click(event.pos)  # 判斷是否點到換檔按鈕
                if isinstance(new_speed, (int, float)):  # Q8 還沒寫完時可能回傳別的東西，這裡擋掉
                    car.set_max_speed(new_speed)

        keys = pygame.key.get_pressed()
        if not lap_timer.is_running and any(keys):
            lap_timer.lap()
        handle_movement(keys, car)
        car.update()

        update_high_score(state)
        handle_boundary(car, track_back, state, SPAWN_X, SPAWN_Y, SPAWN_ANGLE, timer=lap_timer)

        score_before_lap = state.score
        update_lap_progress(car, state)
        if state.score > score_before_lap:
            lap_timer.lap()

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

        lap_text = font.render(f"Lap:  {lap_timer.current_lap_str()}", True, (255, 255, 255))
        best_text = font.render(f"Best: {lap_timer.best_lap_str()}", True, (255, 220, 0))
        screen.blit(lap_text, (20, 128))
        screen.blit(best_text, (20, 164))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
