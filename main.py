"""
Главный файл запуска игры
"""

import arcade
from src.game import GameWindow


def main():
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
