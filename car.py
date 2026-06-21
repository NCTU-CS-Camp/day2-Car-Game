import math

import pygame

DEFAULT_MAX_SPEED = 10
ACCEL = 0.2
ROTATE_SPEED = 5
FRICTION = 0.92

def rotation(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def move(point, angle, unit):
    x, y = point
    rad = math.radians(-angle % 360)

    x += unit * math.sin(rad)
    y += unit * math.cos(rad)

    return x, y

class Car:
    def __init__(self, x=120, y=480, angle=180):
        self.width = 17
        self.height = 35
        self.angle = angle
        self.velocity = 0
        self.acceleration = 0
        self.max_speed = DEFAULT_MAX_SPEED
        self._set_position(x, y)

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def _set_position(self, x, y):
        self.x = x
        self.y = y
        self.center = (x, y)
        self.d = (x - self.width / 2, y - self.height / 2)
        self.c = (x + self.width / 2, y - self.height / 2)
        self.b = (x + self.width / 2, y + self.height / 2)
        self.a = (x - self.width / 2, y + self.height / 2)

    def set_accel(self, accel):
        self.acceleration = accel

    def rotate(self, rot):
        self.angle = (self.angle + rot) % 360

    def update(self):
        if self.acceleration != 0:
            self.velocity += self.acceleration
            self.velocity = max(-self.max_speed, min(self.velocity, self.max_speed))
        else:
            self.velocity *= FRICTION

        self.x, self.y = move((self.x, self.y), self.angle, self.velocity)
        self.center = (self.x, self.y)

        self.d = (self.x - self.width / 2, self.y - self.height / 2)
        self.c = (self.x + self.width / 2, self.y - self.height / 2)
        self.b = (self.x + self.width / 2, self.y + self.height / 2)
        self.a = (self.x - self.width / 2, self.y + self.height / 2)

        rad = math.radians(self.angle)
        self.a = rotation(self.center, self.a, rad)
        self.b = rotation(self.center, self.b, rad)
        self.c = rotation(self.center, self.c, rad)
        self.d = rotation(self.center, self.d, rad)

    def collision(self, collision_surface):
        for point in (self.a, self.b, self.c, self.d):
            if collision_surface.get_at((int(point[0]), int(point[1]))).a == 0:
                return True
        return False

    def draw(self, display, car_image):
        rotated_image = pygame.transform.rotate(car_image, -self.angle - 180)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        display.blit(rotated_image, rect)

    def reset(self, x=120, y=480, angle=180):
        self.angle = angle
        self.velocity = 0
        self.acceleration = 0
        self._set_position(x, y)
