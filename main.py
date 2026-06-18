import math
from pathlib import Path

import pygame

from car import Car

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
HIGHSCORE_PATH = Path(__file__).resolve().parent / "highscore.txt"
FPS = 30
SPAWN_X, SPAWN_Y = 120, 480

FINISH_RECT = pygame.Rect(60, 428, 135, 26)
CHECKPOINT_RECT = pygame.Rect(1410, 310, 80, 80)
FINISH_LEAVE_DISTANCE = 200  # must get this far from the line before a lap can arm
MESSAGE_FRAMES = FPS  # how long the "+1 Lap!" / "Crashed!" message stays on screen

GEARS = [("1", 3), ("2", 5), ("3", 8)]  # (button label, speed)
DEFAULT_GEAR = 1
GEAR_BUTTON_SIZE = (50, 40)
GEAR_BUTTON_GAP = 10
GEAR_BUTTON_TOP_RIGHT_MARGIN = 20


def load_high_score():
    try:
        return int(HIGHSCORE_PATH.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(value):
    HIGHSCORE_PATH.write_text(str(value))


def run():
    pygame.init()

    track_front = pygame.image.load(ASSETS_DIR / "track_front.png")
    track_back = pygame.image.load(ASSETS_DIR / "track_back.png")
    car_image = pygame.image.load(ASSETS_DIR / "car.png")

    screen = pygame.display.set_mode(track_front.get_size())
    pygame.display.set_caption("WASD Car")
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

    car = Car(SPAWN_X, SPAWN_Y)
    current_gear = DEFAULT_GEAR
    car.set_speed(GEARS[current_gear][1])

    score = 0
    high_score = load_high_score()
    armed = False  # car has left the finish line and is eligible to arm a new lap
    checkpoint_passed = False  # car has reached the far-side checkpoint this lap
    message = ""
    message_timer = 0

    def register_score_if_record():
        nonlocal high_score
        if score > high_score:
            high_score = score
            save_high_score(high_score)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(gear_buttons):
                    if rect.collidepoint(event.pos):
                        current_gear = i
                        car.set_speed(GEARS[current_gear][1])
                        break

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        car.move(dx, dy)

        if car.collision(track_back):
            register_score_if_record()
            score = 0
            armed = False
            checkpoint_passed = False
            message, message_timer = "Crashed!", MESSAGE_FRAMES
            car.reset(SPAWN_X, SPAWN_Y)

        on_finish_line = FINISH_RECT.collidepoint(car.x, car.y)
        on_checkpoint = CHECKPOINT_RECT.collidepoint(car.x, car.y)
        distance_from_finish = math.hypot(
            car.x - FINISH_RECT.centerx, car.y - FINISH_RECT.centery
        )

        if not armed and distance_from_finish > FINISH_LEAVE_DISTANCE:
            armed = True
            checkpoint_passed = False

        if armed and on_checkpoint:
            checkpoint_passed = True

        if armed and checkpoint_passed and on_finish_line:
            score += 1
            register_score_if_record()
            armed = False
            checkpoint_passed = False
            message, message_timer = "+1 Lap!", MESSAGE_FRAMES

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
