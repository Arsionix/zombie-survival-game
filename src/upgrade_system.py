"""
Система улучшений характеристик игрока
"""

import arcade
import random

class UpgradeSystem:
    def __init__(self, player):
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

    def can_buy(self, upgrade_type):
        level = self.active_upgrades[upgrade_type]
        if level >= len(self.upgrade_config[upgrade_type][1]):
            return False
        cost = self.upgrade_config[upgrade_type][1][level][1]
        return self.points >= cost

    def buy(self, upgrade_type):
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
        level = self.active_upgrades[upgrade_type]
        bonus_pct, _ = self.upgrade_config[upgrade_type][1][level - 1]

        if upgrade_type == 'health':
            self.player.max_health *= (1 + bonus_pct / 100)
            self.player.health = self.player.max_health
        elif upgrade_type == 'speed':
            self.player.speed *= (1 + bonus_pct / 100)
        elif upgrade_type == 'damage':
            if hasattr(self.player, 'damage'):
                self.player.damage *= (1 + bonus_pct / 100)
        elif upgrade_type == 'weapon':
            if hasattr(self.player, 'fire_rate'):
                self.player.fire_rate *= (1 + bonus_pct / 100)
            if hasattr(self.player, 'reload_time'):
                self.player.reload_time *= (1 - bonus_pct / 100)
        elif upgrade_type == 'special':
            pass

    def get_active_upgrades(self):
        return {
            typ: lvl for typ, lvl in self.active_upgrades.items() if lvl > 0
        }

    def draw_active_upgrades(self, x, y):
        arcade.draw_text("АКТИВНЫЕ УЛУЧШЕНИЯ:", x, y, arcade.color.YELLOW, 16, font_name="Impact")
        y_offset = 20
        for typ, lvl in self.get_active_upgrades().items():
            name = self.upgrade_config[typ][0]
            arcade.draw_text(f"{name}: Уровень {lvl}", x, y - y_offset, arcade.color.WHITE, 14, font_name="Impact")
            y_offset += 20

    def draw_upgrade_menu(self, x, y):
        arcade.draw_text("МЕНЮ УЛУЧШЕНИЙ:", x, y, arcade.color.GREEN, 18, font_name="Impact")
        y_offset = 25
        for typ, (name, levels) in self.upgrade_config.items():
            current_lvl = self.active_upgrades[typ]
            if current_lvl < len(levels):
                next_bonus, next_cost = levels[current_lvl]
                status = f"Уровень {current_lvl + 1} (+{next_bonus}%, {next_cost} очков)"
            else:
                status = "Макс. уровень"
            color = arcade.color.WHITE if self.can_buy(typ) else arcade.color.GRAY
            arcade.draw_text(f"{name}: {status}", x, y - y_offset, color, 14, font_name="Impact")
            y_offset += 20

    def add_points(self, amount):
        self.points += amount

    def get_points(self):
        return self.points
