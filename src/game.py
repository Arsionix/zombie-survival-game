import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Zombie Survival"


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        print("Игра запущена!")

    def setup(self):
        pass

    def on_draw(self):
        self.clear(arcade.color.DARK_SLATE_GRAY)


def main():
    window = GameWindow()
    window.setup()
    window.run()


if __name__ == "__main__":
    main()
