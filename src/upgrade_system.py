"""
Система улучшений характеристик игрока
"""

import arcade
from .constants import SCREEN_HEIGHT


class UpgradeSystem:
    def __init__(self, player):
        """
        Инициализирует систему улучшений.
        """
        self.player = player
        self.points = 0

        self.upgrade_config = {
            'health': ('Здоровье', [(20, 100), (40, 250), (60, 500)]),
            'speed': ('Скорость', [(10, 150), (20, 300), (30, 600)]),
            'damage': ('Урон', [(15, 200), (30, 400), (50, 800)]),
            'weapon': ('Оружие', [(20, 300), (40, 600), (60, 1200)]),
            'special': ('Особые способности', [(1, 500), (2, 1000), (3, 2000)])
        }

        self.active_upgrades = {typ: 0 for typ in self.upgrade_config}
        self.max_active = 3
        self.current_active_count = 0

    def draw_upgrade_menu(self, x, y):
        arcade.draw_text("МЕНЮ УЛУЧШЕНИЙ:", x, y,
                         arcade.color.GREEN, 18, font_name="Impact")

        y_offset = 25
        for typ, (name, levels) in self.upgrade_config.items():
            current_lvl = self.active_upgrades[typ]
            if current_lvl < len(levels):
                next_bonus, next_cost = levels[current_lvl]
                status = f"Уровень {current_lvl + 1} (+{next_bonus}%, {next_cost} очков)"
            else:
                status = "Макс. уровень"

            color = arcade.color.WHITE if self.can_buy(
                typ) else arcade.color.GRAY

            arcade.draw_text(f"{name}: {status}", x, y - y_offset,
                             color, 14, font_name="Impact")
            y_offset += 20

        arcade.draw_text(f"Ваши очки: {self.points}", x, y - y_offset - 10,
                         arcade.color.WHITE, 16, font_name="Impact")

    def handle_mouse_click(self, x, y):
        """
        Обрабатывает клик мыши в меню улучшений
        """
        menu_x = 50
        menu_y = SCREEN_HEIGHT - 100

        y_offset = 25
        for typ, (name, levels) in self.upgrade_config.items():
            current_lvl = self.active_upgrades[typ]
            if current_lvl < len(levels):
                text_height = 20
                text_width = 400

                rect_x = menu_x + text_width/2
                rect_y = menu_y - y_offset + text_height/2

                if (rect_x - text_width/2 <= x <= rect_x + text_width/2 and
                        rect_y - text_height/2 <= y <= rect_y + text_height/2):

                    if self.can_buy(typ):
                        if self.buy(typ):
                            print(f"Куплено улучшение {typ}")
                            return True
                    else:
                        print(f"Недостаточно очков или достигнут макс. уровень")
                    break

            y_offset += 20

        return False

    def can_buy(self, upgrade_type):
        """
        Проверяет, можно ли купить улучшение.
        """
        level = self.active_upgrades[upgrade_type]
        if level >= len(self.upgrade_config[upgrade_type][1]):
            return False
        cost = self.upgrade_config[upgrade_type][1][level][1]
        return self.points >= cost

    def buy(self, upgrade_type):
        """
        Покупает улучшение
        """
        if not self.can_buy(upgrade_type):
            return False

        level = self.active_upgrades[upgrade_type]
        cost = self.upgrade_config[upgrade_type][1][level][1]

        if self.current_active_count >= self.max_active and level == 0:
            return False

        self.points -= cost
        self.active_upgrades[upgrade_type] += 1

        if level == 0:
            self.current_active_count += 1

        self.apply_effect(upgrade_type)
        return True

    def apply_effect(self, upgrade_type):
        """
        Применяет эффект улучшения к игроку
        """
        level = self.active_upgrades[upgrade_type]
        bonus_pct, _ = self.upgrade_config[upgrade_type][1][level - 1]

        if upgrade_type == 'health':
            self.player.max_health *= (1 + bonus_pct / 100)
            self.player.health = self.player.max_health
            print(f"Здоровье увеличено до {self.player.max_health}")

        elif upgrade_type == 'speed':
            self.player.speed *= (1 + bonus_pct / 100)
            print(f"Скорость увеличена до {self.player.speed}")

        elif upgrade_type == 'damage':
            if not hasattr(self.player, 'damage'):
                self.player.damage = 1.0
            self.player.damage *= (1 + bonus_pct / 100)
            print(f"Урон увеличен до x{self.player.damage:.2f}")

        elif upgrade_type == 'weapon':
            if not hasattr(self.player, 'fire_rate'):
                self.player.fire_rate = 1.0
            self.player.fire_rate *= (1 + bonus_pct / 100)
            print(f"Скорострельность увеличена до {self.player.fire_rate}")

        elif upgrade_type == 'special':
            print("Особая способность разблокирована!")

    def get_active_upgrades(self):
        active_upgrades = {}
        for upgrade_type, level in self.active_upgrades.items():
        if level > 0:
            active_upgrades[upgrade_type] = level
            
        return active_upgrades

    def draw_active_upgrades(self, x, y):
        """
        Отрисовывает активные улучшения
        """
        arcade.draw_text("АКТИВНЫЕ УЛУЧШЕНИЯ:", x, y,
                         arcade.color.YELLOW, 16, font_name="Impact")
        y_offset = 20
        for typ, lvl in self.get_active_upgrades().items():
            name = self.upgrade_config[typ][0]
            arcade.draw_text(f"{name}: Уровень {lvl}", x, y - y_offset,
                             arcade.color.WHITE, 14, font_name="Impact")
            y_offset += 20

    def add_points(self, amount):
        self.points += amount

    def get_points(self):
        return self.points
