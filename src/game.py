"""Основной класс игры"""

import arcade
from .constants import *


class GameWindow(arcade.Window):
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE):
        super().__init__(width, height, title)
        arcade.set_background_color(BACKGROUND_COLOR)

    def setup(self):
        """Настройка игры"""

    def on_draw(self):
        """Отрисовка"""
        self.clear()
