import pygame

from car import ACCEL, ROTATE_SPEED


def handle_movement(keys, car):
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
