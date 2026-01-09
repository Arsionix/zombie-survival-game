import arcade
import math
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .bullet import Bullet


class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.change_x = 0
        self.change_y = 0
        self.angle = 0
        self.shoot_timer = 0
        self.shoot_cooldown = 0.3

    def update(self):
        self.x += self.change_x
        self.y += self.change_y

        if self.shoot_timer > 0:
            self.shoot_timer -= 1/60

        if self.x < 20:
            self.x = 20
        if self.x > SCREEN_WIDTH - 20:
            self.x = SCREEN_WIDTH - 20
        if self.y < 20:
            self.y = 20
        if self.y > SCREEN_HEIGHT - 20:
            self.y = SCREEN_HEIGHT - 20

    def draw(self):
        arcade.draw_rect_filled(arcade.rect.XYWH(
            self.x, self.y, 40, 40), arcade.color.BLUE)

        end_x = self.x + math.cos(math.radians(self.angle)) * 30
        end_y = self.y + math.sin(math.radians(self.angle)) * 30
        arcade.draw_line(self.x, self.y, end_x, end_y, arcade.color.YELLOW, 3)

    def rotate_to(self, mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))

    def shoot(self):
        if self.shoot_timer <= 0:
            bullet = Bullet(self.x, self.y, self.angle)
            self.shoot_timer = self.shoot_cooldown
            return bullet
        return None
