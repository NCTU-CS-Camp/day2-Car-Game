from pathlib import Path

import pygame

from car import ACCEL, ROTATE_SPEED, Car
from race import GearButtons, RaceState

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
    race = RaceState()

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
        if keys[pygame.K_w]:
            car.set_accel(ACCEL)
        elif keys[pygame.K_s]:
            car.set_accel(-ACCEL)
        else:
            car.set_accel(0)
        if keys[pygame.K_j]:
            car.rotate(-ROTATE_SPEED)
        if keys[pygame.K_k]:
            car.rotate(ROTATE_SPEED)
        car.update()

        if car.collision(track_back):
            race.handle_crash()
            car.reset(SPAWN_X, SPAWN_Y, SPAWN_ANGLE)

        race.update(car)

        screen.blit(track_front, (0, 0))
        car.draw(screen, car_image)
        race.draw(screen, font)
        gear_buttons.draw(screen, font)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()
