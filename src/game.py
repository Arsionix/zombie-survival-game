"""
Основной класс игры - связывает всё вместе
"""

import arcade
from .constants import *
from .player import Player
from .bullet import Bullet


class GameWindow(arcade.Window):
    """Главное окно игры"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player = None
        self.bullets = []

        self.mouse_x = SCREEN_WIDTH // 2
        self.mouse_y = SCREEN_HEIGHT // 2

    def setup(self):
        """Настройка начального состояния игры"""
        self.player = Player()
        self.bullets = []

        self.set_mouse_visible(True)

    def on_draw(self):
        self.clear()

        self.player.draw()

        for bullet in self.bullets:
            bullet.draw()

    def on_update(self, delta_time):
        """Обновление игровой логики"""
        self.player.update(delta_time)

        self.player.face_mouse(self.mouse_x, self.mouse_y)

        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.update()
            if bullet.is_off_screen():
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        self.player.on_key_release(key)

    def on_mouse_motion(self, x, y, dx, dy):
        """Движение мыши - для поворота игрока"""
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        """Нажатие мыши - стрельба (завтра)"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            pass
