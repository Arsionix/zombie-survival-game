"""
Основной класс игры
"""

import arcade
from .constants import *
from .player import Player


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player = None
        self.zombies = None
        self.bullets = None

    def setup(self):
        """Настройка начального состояния игры"""
        self.player = Player()
        self.zombies = arcade.SpriteList()
        self.bullets = arcade.SpriteList()

    def on_draw(self):
        """Отрисовка игры"""
        self.clear(BACKGROUND_COLOR)
        self.player.draw()
        self.zombies.draw()
        self.bullets.draw()

    def on_update(self, delta_time):
        """Обновление логики игры"""
        self.player.update()

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        pass

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия мыши"""
        pass
