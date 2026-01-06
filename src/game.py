import arcade
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR
from .player import Player


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)
        self.keys = {}

    def setup(self):
        self.player = Player()

    def on_draw(self):
        self.clear()
        self.player.draw()

    def on_update(self, delta_time):
        self.player.change_x = 0
        self.player.change_y = 0

        if self.keys.get(arcade.key.W) or self.keys.get(arcade.key.UP):
            self.player.change_y = self.player.speed
        if self.keys.get(arcade.key.S) or self.keys.get(arcade.key.DOWN):
            self.player.change_y = -self.player.speed
        if self.keys.get(arcade.key.A) or self.keys.get(arcade.key.LEFT):
            self.player.change_x = -self.player.speed
        if self.keys.get(arcade.key.D) or self.keys.get(arcade.key.RIGHT):
            self.player.change_x = self.player.speed

        self.player.update()

    def on_key_press(self, key, modifiers):
        self.keys[key] = True

    def on_key_release(self, key, modifiers):
        self.keys[key] = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.rotate_to(x, y)
