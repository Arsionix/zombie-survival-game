"""
Класс игрока с управлением и анимацией
"""

import arcade
import math
import time


class Player:
    """Игрок с управлением WASD и анимацией"""

    def __init__(self):
        from .constants import (
            PLAYER_START_X, PLAYER_START_Y,
            PLAYER_SIZE, PLAYER_COLOR, PLAYER_NOSE_COLOR
        )

        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

        self.speed = 5
        self.change_x = 0
        self.change_y = 0

        self.color = PLAYER_COLOR
        self.nose_color = PLAYER_NOSE_COLOR
        self.angle = 0

        self.state = 0
        self.animation_time = 0
        self.animation_speed = 10
        self.walk_offset = 0

        self.keys_pressed = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }

    def update(self, delta_time):
        """Обновление состояния игрока"""
        from .constants import SCREEN_WIDTH, SCREEN_HEIGHT

        self.animation_time += delta_time

        dx, dy = 0, 0

        if self.keys_pressed['up']:
            dy += 1
        if self.keys_pressed['down']:
            dy -= 1
        if self.keys_pressed['left']:
            dx -= 1
        if self.keys_pressed['right']:
            dx += 1

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.change_x = dx * self.speed
        self.change_y = dy * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y

        half_width = self.width / 2
        half_height = self.height / 2

        self.center_x = max(half_width, min(
            SCREEN_WIDTH - half_width, self.center_x))
        self.center_y = max(half_height, min(
            SCREEN_HEIGHT - half_height, self.center_y))

        is_moving = dx != 0 or dy != 0
        self.state = 1 if is_moving else 0

        if is_moving:
            self.walk_offset = math.sin(
                self.animation_time * self.animation_speed) * 3
        else:
            self.walk_offset = 0

    def draw(self):
        """Отрисовка игрока с анимацией"""
        from .constants import PLAYER_SIZE

        y_offset = self.walk_offset

        arcade.draw_rect_filled(arcade.rect.XYWH(
            self.center_x, self.center_y + y_offset, self.width, self.height), self.color, self.angle)

        nose_distance = PLAYER_SIZE / 2 + 10
        nose_x = self.center_x + \
            math.cos(math.radians(self.angle)) * nose_distance
        nose_y = self.center_y + y_offset + \
            math.sin(math.radians(self.angle)) * nose_distance

        arcade.draw_rect_filled(arcade.rect.XYWH(
            nose_x, nose_y, 15, 8), self.nose_color, self.angle)

        eye_offset = PLAYER_SIZE * 0.25
        eye_y_offset = PLAYER_SIZE * 0.1

        left_eye_x = self.center_x + \
            math.cos(math.radians(self.angle + 90)) * eye_offset
        left_eye_y = self.center_y + y_offset + \
            math.sin(math.radians(self.angle + 90)) * eye_offset + eye_y_offset

        right_eye_x = self.center_x + \
            math.cos(math.radians(self.angle - 90)) * eye_offset
        right_eye_y = self.center_y + y_offset + \
            math.sin(math.radians(self.angle - 90)) * eye_offset + eye_y_offset

        arcade.draw_circle_filled(
            left_eye_x, left_eye_y, 5, arcade.color.WHITE)
        arcade.draw_circle_filled(
            right_eye_x, right_eye_y, 5, arcade.color.WHITE)

        pupil_offset = 2
        arcade.draw_circle_filled(
            left_eye_x + math.cos(math.radians(self.angle)) * pupil_offset,
            left_eye_y + math.sin(math.radians(self.angle)) * pupil_offset,
            2, arcade.color.BLACK
        )
        arcade.draw_circle_filled(
            right_eye_x + math.cos(math.radians(self.angle)) * pupil_offset,
            right_eye_y + math.sin(math.radians(self.angle)) * pupil_offset,
            2, arcade.color.BLACK
        )

    def face_mouse(self, mouse_x, mouse_y):
        """Поворачивает игрока к курсору мыши"""
        dx = mouse_x - self.center_x
        dy = mouse_y - self.center_y

        if dx != 0 or dy != 0:
            self.angle = math.degrees(math.atan2(dy, dx))

    def on_key_press(self, key):
        """Обработка нажатия клавиш"""
        if key in (arcade.key.W, arcade.key.UP):
            self.keys_pressed['up'] = True
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.keys_pressed['down'] = True
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.keys_pressed['left'] = True
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.keys_pressed['right'] = True

    def on_key_release(self, key):
        """Обработка отпускания клавиш"""
        if key in (arcade.key.W, arcade.key.UP):
            self.keys_pressed['up'] = False
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.keys_pressed['down'] = False
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.keys_pressed['left'] = False
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.keys_pressed['right'] = False
