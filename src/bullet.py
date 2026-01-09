import arcade
import math
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 10
        self.angle = angle

        self.change_x = math.cos(math.radians(angle)) * self.speed
        self.change_y = math.sin(math.radians(angle)) * self.speed

    def update(self):
        self.x += self.change_x
        self.y += self.change_y

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, 5, arcade.color.RED)

    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT)
