"""
Главный файл запуска игры
"""

import arcade
from src.ui import MenuView
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    """
    Инициализирует окно игры и запускает главное меню.
    """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
