"""
Класс пули (базовый, для стрельбы завтра)
"""

import arcade
import math


class Bullet:
    """Пуля, выпущенная игроком"""

    def __init__(self, start_x, start_y, target_x, target_y):
        from .constants import SCREEN_WIDTH, SCREEN_HEIGHT

        self.x = start_x
        self.y = start_y
        self.radius = 5
        self.speed = 10
        self.color = arcade.color.YELLOW

        dx = target_x - start_x
        dy = target_y - start_y
        distance = max(0.1, math.sqrt(dx*dx + dy*dy))

        self.dx = (dx / distance) * self.speed
        self.dy = (dy / distance) * self.speed

    def update(self):
        """Обновление позиции пули"""
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        """Отрисовка пули"""
        arcade.draw_circle_filled(
            center_x=self.x,
            center_y=self.y,
            radius=self.radius,
            color=self.color
        )

    def is_off_screen(self):
        """Проверка, вышла ли пуля за экран"""
        from .constants import SCREEN_WIDTH, SCREEN_HEIGHT
        return (self.x < -self.radius or self.x > SCREEN_WIDTH + self.radius or
                self.y < -self.radius or self.y > SCREEN_HEIGHT + self.radius)
