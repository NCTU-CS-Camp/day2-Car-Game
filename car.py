import math

import pygame

DEFAULT_MAX_SPEED = 10
ACCEL = 0.2
ROTATE_SPEED = 5
FRICTION = 0.92

def rotation(origin, point, angle):
    """
    功能：將指定座標點繞原點旋轉。
    參數：origin 為旋轉中心，point 為目標座標，angle 為弧度。
    回傳值：旋轉後的 (x, y) 座標。
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def move(point, angle, unit):
    """
    功能：依指定角度與距離移動座標點。
    參數：point 為起始座標，angle 為角度，unit 為移動距離。
    回傳值：移動後的 (x, y) 座標。
    """
    x, y = point
    rad = math.radians(-angle % 360)

    x += unit * math.sin(rad)
    y += unit * math.cos(rad)

    return x, y

class Car:
    def __init__(self, x=120, y=480, angle=180):
        """
        功能：建立並初始化車輛物件。
        參數：x、y 為初始位置，angle 為初始角度。
        回傳值：無。
        """
        self.width = 17
        self.height = 35
        self.angle = angle
        self.velocity = 0
        self.acceleration = 0
        self.max_speed = DEFAULT_MAX_SPEED
        self._set_position(x, y)

    def set_max_speed(self, max_speed):
        """
        功能：設定車輛的最高速度。
        參數：max_speed 為新的最高速度。
        回傳值：無。
        """
        self.max_speed = max_speed

    def _set_position(self, x, y):
        """
        功能：設定車輛中心位置及四個角點座標。
        參數：x、y 為車輛中心座標。
        回傳值：無。
        """
        self.x = x
        self.y = y
        self.center = (x, y)
        self.d = (x - self.width / 2, y - self.height / 2)
        self.c = (x + self.width / 2, y - self.height / 2)
        self.b = (x + self.width / 2, y + self.height / 2)
        self.a = (x - self.width / 2, y + self.height / 2)

    def set_accel(self, accel):
        """
        功能：設定車輛的加速度。
        參數：accel 為新的加速度。
        回傳值：無。
        """
        self.acceleration = accel

    def rotate(self, rot):
        """
        功能：調整車輛目前的旋轉角度。
        參數：rot 為要增加或減少的角度。
        回傳值：無。
        """
        self.angle = (self.angle + rot) % 360

    def update(self):
        """
        功能：更新車輛速度、位置及四個角點座標。
        參數：無。
        回傳值：無。
        """
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
        """
        功能：檢查車輛四個角點是否碰撞賽道邊界。
        參數：collision_surface 為用於碰撞判定的 Pygame 圖層。
        回傳值：發生碰撞時回傳 True，否則回傳 False。
        """
        for point in (self.a, self.b, self.c, self.d):
            if collision_surface.get_at((int(point[0]), int(point[1]))).a == 0:
                return True
        return False

    def draw(self, display, car_image):
        """
        功能：依車輛位置與角度將圖片繪製到畫面。
        參數：display 為顯示畫面，car_image 為車輛圖片。
        回傳值：無。
        """
        rotated_image = pygame.transform.rotate(car_image, -self.angle - 180)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        display.blit(rotated_image, rect)

    def reset(self, x=120, y=480, angle=180):
        """
        功能：重設車輛的位置、角度、速度及加速度。
        參數：x、y 為重設位置，angle 為重設角度。
        回傳值：無。
        """
        self.angle = angle
        self.velocity = 0
        self.acceleration = 0
        self._set_position(x, y)
