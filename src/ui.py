import arcade
import arcade.gui
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_texture = None
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.setup()

    def setup(self):
        self.background_texture = arcade.load_texture("menu_backround.jpg")

        start_button_style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                font_size=20,
                font_name=("Impact", "Arial Black", "Arial"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.DARK_RED,
                border=arcade.color.BROWN,
                border_width=4
            ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                font_size=20,
                font_name=("Impact", "Arial Black", "Arial"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.RED_DEVIL,
                border=arcade.color.DARK_RED,
                border_width=4
            ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                font_size=18,
                font_name=("Impact", "Arial Black", "Arial"),
                font_color=arcade.color.LIGHT_GRAY,
                bg=arcade.color.BLACK,
                border=arcade.color.DARK_RED,
                border_width=4
            )
        }

        button_style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                font_size=16,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.LIGHT_GRAY,
                bg=arcade.color.BROWN,
                border=arcade.color.DARK_RED,
                border_width=2
            ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                font_size=17,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.DARK_RED,
                border=arcade.color.RED,
                border_width=2
            ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                font_size=15,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.DARK_RED,
                border=arcade.color.BLACK,
                border_width=2
            )
        }

        start_button = arcade.gui.UIFlatButton(text="НАЧАТЬ ИГРУ", width=400, height=50, style=start_button_style)
        wins_button = arcade.gui.UIFlatButton(text="РЕКОРДЫ", width=195, height=50, style=button_style)
        settings_button = arcade.gui.UIFlatButton(text="НАСТРОЙКИ", width=195, height=50, style=button_style)
        exit_button = arcade.gui.UIFlatButton(text="ВЫХОД", width=100, height=30, style=button_style)

        start_button.on_click = self.start_game
        wins_button.on_click = self.wins_view
        settings_button.on_click = self.settings_window
        exit_button.on_click = self.exit_action

        self.uimanager.add(start_button)
        self.uimanager.add(wins_button)
        self.uimanager.add(settings_button)
        self.uimanager.add(exit_button)

        start_button.center_x = self.window.width // 2
        start_button.center_y = self.window.height // 2

        wins_button.center_x = self.window.width // 2 - 100
        wins_button.center_y = self.window.height // 2 - 80

        settings_button.center_x = self.window.width // 2 + 100
        settings_button.center_y = self.window.height // 2 - 80

        exit_button.center_x = self.window.width - 80
        exit_button.center_y = self.window.height - 40

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(arcade.load_texture("menu_backround.jpg"),
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.uimanager.draw()

    def start_game(self, event):
        from main import GameView
        game_view = GameView()
        self.window.show_view(game_view)

    def wins_view(self, event):
        records_view = RecordsView(previous_view=self)
        self.window.show_view(records_view)

    def settings_window(self, event):
        settings_view = SettingView(previous_view=self)
        self.window.show_view(settings_view)

    def exit_action(self, event):
        arcade.close_window()

class SettingView(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.setup()

    def setup(self):
        self.uimanager.clear()

        button_style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                font_size=16,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.LIGHT_GRAY,
                bg=arcade.color.BROWN,
                border=arcade.color.DARK_RED,
                border_width=2
            ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                font_size=17,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.DARK_RED,
                border=arcade.color.RED,
                border_width=2
            ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                font_size=15,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.DARK_RED,
                border=arcade.color.BLACK,
                border_width=2
            )
        }

        volume_slider = arcade.gui.UISlider(value=50, width=400, height=20, x=(SCREEN_WIDTH // 2) - 150, y=(SCREEN_HEIGHT // 2) + 150)
        self.uimanager.add(volume_slider)

        back_button = arcade.gui.UIFlatButton(text="НАЗАД", width=100, height=30, style=button_style, x=20, y=self.height - 50)
        back_button.on_click = self.on_back_click
        self.uimanager.add(back_button)

        save_button = arcade.gui.UIFlatButton(text="СОХРАНИТЬ", width=200, height=50, x=(self.width // 2) - 100, y=20, style=button_style)
        save_button.on_click = self.on_save_click
        self.uimanager.add(save_button)

    def on_back_click(self, event):
        self.window.show_view(self.previous_view)

    def on_save_click(self, event):
        print("Настройки сохранены!")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.uimanager.enable()

    def on_draw(self):
        self.clear()
        arcade.draw_text("НАСТРОЙКИ", self.window.width // 2, self.window.height - 100,
                         arcade.color.BLACK, font_size=30, anchor_x="center", font_name="Impact")
        arcade.draw_text("Громкость:", (self.window.width // 2) - 100, (self.window.height // 2) + 200,
                         arcade.color.BLACK, font_size=20, anchor_x="center", font_name="Impact")
        self.uimanager.draw()


class RecordsView(arcade.View):
    pass


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_texture = None
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.setup()

    def setup(self):
        button_style = {
            "normal": arcade.gui.UIFlatButton.UIStyle(
                font_size=16,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.BROWN,
                border=arcade.color.DARK_RED,
                border_width=2
            ),
            "hover": arcade.gui.UIFlatButton.UIStyle(
                font_size=17,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.DARK_RED,
                border=arcade.color.RED,
                border_width=2
            ),
            "press": arcade.gui.UIFlatButton.UIStyle(
                font_size=15,
                font_name=("Courier New", "monospace"),
                font_color=arcade.color.BLACK,
                bg=arcade.color.DARK_RED,
                border=arcade.color.BLACK,
                border_width=2
            )
        }

        back_to_menu_button = arcade.gui.UIFlatButton(text="ГЛАВНОЕ МЕНЮ", width=195, height=50, style=button_style)
        start_again_button = arcade.gui.UIFlatButton(text="НАЧАТЬ ЗАНОВО", width=195, height=50, style=button_style)

        back_to_menu_button.on_click = self.back_to_main_menu
        start_again_button.on_click = self.start_game_again

        self.uimanager.add(back_to_menu_button)
        self.uimanager.add(start_again_button)

        back_to_menu_button.center_x = self.window.width // 2 - 100
        back_to_menu_button.center_y = self.window.height // 2 - 80

        start_again_button.center_x = self.window.width // 2 + 100
        start_again_button.center_y = self.window.height // 2 - 80

    def on_draw(self):
        self.clear()
        arcade.draw_rect_filled(arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                                arcade.color.BLACK)
        arcade.draw_text(f"Финальный счёт игры: {self.final_score}",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40,
                         arcade.color.WHITE, font_size=24, anchor_x="center")
        arcade.draw_text(f"Достигнутая волна: {self.final_wave}",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        self.uimanager.draw()

    def start_game_again(self, event):
        from main import GameView
        game_view = GameView()
        self.window.show_view(game_view)

    def back_to_main_menu(self, event):
        main_menu_view = MenuView()
        self.window.show_view(main_menu_view)
