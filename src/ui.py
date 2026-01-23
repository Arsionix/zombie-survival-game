import arcade
import arcade.gui
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT


class MenuView(arcade.View):
    def __init__(self):
        """
        Инициализирует главное меню.
        """
        super().__init__()
        self.background_texture = None
        self.uimanager = arcade.gui.UIManager()
        self.setup()

    def setup(self):
        """
        Настраивает элементы интерфейса главного меню.
        """
        self.background_texture = arcade.load_texture(
            "assets/images/ui/menu_background.jpg")

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

        start_button = arcade.gui.UIFlatButton(
            text="НАЧАТЬ ИГРУ", width=400, height=50, style=start_button_style)
        wins_button = arcade.gui.UIFlatButton(
            text="РЕКОРДЫ", width=195, height=50, style=button_style)
        settings_button = arcade.gui.UIFlatButton(
            text="НАСТРОЙКИ", width=195, height=50, style=button_style)
        exit_button = arcade.gui.UIFlatButton(
            text="ВЫХОД", width=100, height=30, style=button_style)

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

    def on_show_view(self):
        """
        Вызывается при показе главного меню.
        """
        self.uimanager.enable()
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_hide_view(self):
        """
        Вызывается при скрытии главного меню.
        """
        self.uimanager.disable()

    def on_draw(self):
        """
        Отрисовывает главное меню.
        """
        self.clear()
        arcade.draw_texture_rect(arcade.load_texture("assets/images/ui/menu_background.jpg"),
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.uimanager.draw()

    def start_game(self, event):
        """
        Обрабатывает нажатие кнопки начала игры.
        """
        from .game import GameView
        self.uimanager.disable()
        game_view = GameView()
        self.window.show_view(game_view)

    def wins_view(self, event):
        """
        Обрабатывает нажатие кнопки просмотра рекордов.
        """
        self.uimanager.disable()
        records_view = RecordsView()
        self.window.show_view(records_view)

    def settings_window(self, event):
        """
        Обрабатывает нажатие кнопки настроек.
        """
        self.uimanager.disable()
        settings_view = SettingView(previous_view=self)
        self.window.show_view(settings_view)

    def exit_action(self, event):
        """
        Обрабатывает нажатие кнопки выхода из игры.
        """
        arcade.close_window()


class SettingView(arcade.View):
    def __init__(self, previous_view):
        """
        Инициализирует экран настроек.
        """
        super().__init__()
        self.previous_view = previous_view
        self.uimanager = arcade.gui.UIManager()
        self.setup()

    def setup(self):
        """
        Настраивает элементы интерфейса настроек.
        """
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

        volume_slider = arcade.gui.UISlider(value=50, width=400, height=20, x=(
            SCREEN_WIDTH // 2) - 150, y=(SCREEN_HEIGHT // 2) + 150)
        self.uimanager.add(volume_slider)

        back_button = arcade.gui.UIFlatButton(
            text="НАЗАД", width=100, height=30, style=button_style, x=20, y=self.height - 50)
        back_button.on_click = self.on_back_click
        self.uimanager.add(back_button)

        save_button = arcade.gui.UIFlatButton(text="СОХРАНИТЬ", width=200, height=50, x=(
            self.width // 2) - 100, y=20, style=button_style)
        save_button.on_click = self.on_save_click
        self.uimanager.add(save_button)

    def on_back_click(self, event):
        """
        Обрабатывает нажатие кнопки возврата.
        """
        self.uimanager.disable()
        self.window.show_view(self.previous_view)

    def on_save_click(self, event):
        """
        Обрабатывает нажатие кнопки сохранения настроек.
        """
        print("Настройки сохранены!")

    def on_show_view(self):
        """
        Вызывается при показе экрана настроек.
        """
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.uimanager.enable()

    def on_hide_view(self):
        """
        Вызывается при скрытии экрана настроек.
        """
        self.uimanager.disable()

    def on_draw(self):
        """
        Отрисовывает экран настроек.
        """
        self.clear()
        arcade.draw_text("НАСТРОЙКИ", self.window.width // 2, self.window.height - 100,
                         arcade.color.BLACK, font_size=30, anchor_x="center", font_name="Impact")
        arcade.draw_text("Громкость:", (self.window.width // 2) - 100, (self.window.height // 2) + 200,
                         arcade.color.BLACK, font_size=20, anchor_x="center", font_name="Impact")
        self.uimanager.draw()


class RecordsView(arcade.View):
    def __init__(self):
        """
        Инициализирует экран рекордов.
        """
        super().__init__()
        self.uimanager = arcade.gui.UIManager()
        self.setup()

    def setup(self):
        """
        Настраивает элементы интерфейса экрана рекордов.
        """
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

        back_button = arcade.gui.UIFlatButton(
            text="НАЗАД", width=100, height=30, style=button_style, x=20, y=self.height - 50
        )
        back_button.on_click = self.on_back_click
        self.uimanager.add(back_button)

    def on_show_view(self):
        """
        Вызывается при показе экрана рекордов.
        """
        self.uimanager.enable()
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_hide_view(self):
        """
        Вызывается при скрытии экрана рекордов.
        """
        self.uimanager.disable()

    def on_back_click(self, event):
        """
        Обрабатывает нажатие кнопки возврата.
        """
        self.uimanager.disable()
        from .ui import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def on_draw(self):
        """
        Отрисовывает экран рекордов.
        """
        self.clear()
        arcade.set_background_color(arcade.color.DARK_BLUE)

        arcade.draw_text("РЕКОРДЫ", self.window.width // 2, self.window.height - 100,
                         arcade.color.WHITE, font_size=40, anchor_x="center", font_name="Impact")

        arcade.draw_text("Рекорды пока не доступны",
                         self.window.width // 2, self.window.height // 2,
                         arcade.color.LIGHT_GRAY, font_size=24, anchor_x="center", font_name="Impact")

        self.uimanager.draw()


class GameOverView(arcade.View):
    def __init__(self):
        """
        Инициализирует экран окончания игры.
        """
        super().__init__()
        self.background_texture = None
        self.uimanager = arcade.gui.UIManager()
        self.setup()

    def setup(self):
        """
        Настраивает элементы интерфейса экрана окончания игры.
        """
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

        back_to_menu_button = arcade.gui.UIFlatButton(
            text="ГЛАВНОЕ МЕНЮ", width=195, height=50, style=button_style)
        start_again_button = arcade.gui.UIFlatButton(
            text="НАЧАТЬ ЗАНОВО", width=195, height=50, style=button_style)

        back_to_menu_button.on_click = self.back_to_main_menu
        start_again_button.on_click = self.start_game_again

        self.uimanager.add(back_to_menu_button)
        self.uimanager.add(start_again_button)

        back_to_menu_button.center_x = self.window.width // 2 - 100
        back_to_menu_button.center_y = self.window.height // 2 - 80

        start_again_button.center_x = self.window.width // 2 + 100
        start_again_button.center_y = self.window.height // 2 - 80

    def on_show_view(self):
        """
        Вызывается при показе экрана окончания игры.
        """
        self.uimanager.enable()

    def on_hide_view(self):
        """
        Вызывается при скрытии экрана окончания игры.
        """
        self.uimanager.disable()

    def on_draw(self):
        """
        Отрисовывает экран окончания игры.
        """
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
        """
        Обрабатывает нажатие кнопки начала новой игры.
        """
        self.uimanager.disable()
        from .game import GameView
        game_view = GameView()
        self.window.show_view(game_view)

    def back_to_main_menu(self, event):
        """
        Обрабатывает нажатие кнопки возврата в главное меню.
        """
        self.uimanager.disable()
        main_menu_view = MenuView()
        self.window.show_view(main_menu_view)
