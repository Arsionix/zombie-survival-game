import sys
import os
from src.game import GameWindow
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def main():
    game = GameWindow()
    game.setup()
    game.run()


if __name__ == "__main__":
    main()
