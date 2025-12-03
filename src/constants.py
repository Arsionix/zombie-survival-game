"""
Константы игры
"""

import arcade

# Окно
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Zombie Survival"

# Игрок
PLAYER_SPEED = 5
PLAYER_START_X = SCREEN_WIDTH // 2
PLAYER_START_Y = SCREEN_HEIGHT // 2
PLAYER_SIZE = 40

# Состояния анимации
PLAYER_IDLE = 0
PLAYER_MOVING = 1

# Цвета
BACKGROUND_COLOR = arcade.color.DARK_SLATE_GRAY
PLAYER_COLOR = arcade.color.BLUE
PLAYER_NOSE_COLOR = arcade.color.YELLOW
UI_COLOR = arcade.color.WHITE
