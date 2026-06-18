import math

import pygame

from geometry import rotation

DEFAULT_SPEED = 5
TURN_SPEED = 8  # max degrees the heading turns per frame


class Car:
    def __init__(self, x=120, y=480):
        self.width = 17
        self.height = 35
        self.angle = 0  # 0 = facing up, clockwise: 90 right, 180 down, 270 left
        self.speed = DEFAULT_SPEED
        self._set_position(x, y)

    def set_speed(self, speed):
        self.speed = speed

    def _set_position(self, x, y):
        self.x = x
        self.y = y
        self.center = (x, y)
        self.d = (x - self.width / 2, y - self.height / 2)
        self.c = (x + self.width / 2, y - self.height / 2)
        self.b = (x + self.width / 2, y + self.height / 2)
        self.a = (x - self.width / 2, y + self.height / 2)

    def _turn_towards(self, target_angle):
        diff = (target_angle - self.angle + 180) % 360 - 180
        if abs(diff) <= TURN_SPEED:
            self.angle = target_angle
        else:
            self.angle = (self.angle + TURN_SPEED * (1 if diff > 0 else -1)) % 360

    def _update_corners(self):
        x, y = self.x, self.y
        self.d = (x - self.width / 2, y - self.height / 2)
        self.c = (x + self.width / 2, y - self.height / 2)
        self.b = (x + self.width / 2, y + self.height / 2)
        self.a = (x - self.width / 2, y + self.height / 2)

        rad = math.radians(self.angle)
        self.a = rotation(self.center, self.a, rad)
        self.b = rotation(self.center, self.b, rad)
        self.c = rotation(self.center, self.c, rad)
        self.d = rotation(self.center, self.d, rad)

    def move(self, dx, dy):
        length = math.hypot(dx, dy)
        if length != 0:
            target_angle = math.degrees(math.atan2(dx, -dy)) % 360
            self._turn_towards(target_angle)

            self.x += self.speed * dx / length
            self.y += self.speed * dy / length
            self.center = (self.x, self.y)

        self._update_corners()

    def collision(self, collision_surface):
        for point in (self.a, self.b, self.c, self.d):
            if collision_surface.get_at((int(point[0]), int(point[1]))).a == 0:
                return True
        return False

    def draw(self, display, car_image):
        rotated_image = pygame.transform.rotate(car_image, -self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        display.blit(rotated_image, rect)

    def reset(self, x=120, y=480):
        self.angle = 0
        self._set_position(x, y)
