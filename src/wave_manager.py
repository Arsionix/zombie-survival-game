"""
Класс смены волн
"""

import arcade
import random
from .constants import (SCREEN_HEIGHT, SCREEN_WIDTH)
from .zombie import Zombie
from .upgrade_system import UpgradeSystem

SPAWN_MARGIN = 100
COLOR_WAVE_SCREEN = arcade.color.BLACK


class WaveManager:
    def __init__(self, player):
        self.player = player
        self.upgrade_system = UpgradeSystem(player)
        self.show_upgrade_menu = False
        self.current_wave = 0
        self.zombies = []
        self.zombies_to_spawn = 0
        self.zombies_spawned = 0
        self.zombies_killed = 0
        self.wave_active = False
        self.wave_start_delay = 3.0
        self.wave_timer = 0
        self.spawn_interval = 1.0
        self.spawn_timer = 0
        self.types = ["basic", "fast", "fat", "toxic"]
        self.show_player = True
        self.wave_stats = {}
        self.wave_time = 0.0
        self.total_kills_this_wave = 0
        self.show_upgrade_hint = False
        self.upgrade_hint_timer = 0
        self.previous_wave_stats = {"total_damage": 0, "kills": 0, "time": 0.0}

        self.show_wave_screen = False
        self.wave_screen_timer = 0

    def on_mouse_press(self, x, y, button):
        if self.show_upgrade_menu and button == arcade.MOUSE_BUTTON_LEFT:
            if self.upgrade_system.handle_mouse_click(x, y):
                self.show_upgrade_hint = True
                self.upgrade_hint_timer = 2.0

    def start_next_wave(self):
        self.previous_wave_stats = self.wave_stats.copy()

        self.current_wave += 1

        self.wave_active = False
        self.show_upgrade_menu = False
        self.show_wave_screen = True
        self.wave_screen_timer = 2.0

        self.wave_timer = 0
        self.wave_time = 0.0
        self.total_kills_this_wave = 0
        self.zombies_to_spawn = 5 + self.current_wave * 2
        self.zombies_spawned = 0
        self.zombies_killed = 0
        self.show_player = False

        self.zombies.clear()

        self.wave_stats = {
            "total_damage": 0,
            "kills": 0,
            "time": 0.0
        }

    def update(self, delta_time):
        if self.show_wave_screen:
            self.wave_screen_timer -= delta_time
            if self.wave_screen_timer <= 0:
                self.show_wave_screen = False

                if self.current_wave == 1:
                    self.wave_active = True
                    self.show_player = True
                    self.wave_timer = self.wave_start_delay
                else:
                    self.show_upgrade_menu = True
            return

        if self.show_upgrade_menu:
            if self.show_upgrade_hint:
                self.upgrade_hint_timer -= delta_time
                if self.upgrade_hint_timer <= 0:
                    self.show_upgrade_hint = False
            return

        if not self.wave_active:
            self.wave_timer += delta_time
            if self.wave_timer >= self.wave_start_delay:
                self.wave_active = True
                self.show_player = True

        else:
            self.wave_time += delta_time
            self.wave_stats["time"] = self.wave_time

            self.wave_stats["kills"] = self.total_kills_this_wave

            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval and self.zombies_spawned < self.zombies_to_spawn:
                self.spawn_zombie()
                self.spawn_timer = 0

            for zombie in self.zombies[:]:
                zombie.update(delta_time)

            if self.zombies_spawned >= self.zombies_to_spawn and self.zombies_killed >= self.zombies_spawned:
                self.start_next_wave()

    def spawn_zombie(self):
        """
        Создает нового зомби на случайной стороне экрана
        """
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x = random.randint(-SPAWN_MARGIN, 0)
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == "right":
            x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + SPAWN_MARGIN)
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == "top":
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + SPAWN_MARGIN)
        else:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-SPAWN_MARGIN, 0)

        weights = [50, 20, 15, 15]
        if self.current_wave >= 3:
            weights = [40, 25, 20, 15]
        if self.current_wave >= 5:
            weights = [30, 25, 25, 20]

        z_type = random.choices(self.types, weights=weights)[0]
        zombie = Zombie(x, y, z_type, self.current_wave)
        zombie.ai = Zombie.AI(zombie, self.player)
        self.zombies.append(zombie)
        self.zombies_spawned += 1

    def kill_zombie(self, zombie):
        if zombie in self.zombies:
            self.zombies.remove(zombie)
        points = zombie.on_death()
        self.zombies_killed += 1
        self.total_kills_this_wave += 1
        self.upgrade_system.add_points(points)
        return points

    def draw_wave_screen(self):
        arcade.draw_rect_filled(arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                                arcade.color.BLACK)

        arcade.draw_text(f"ВОЛНА {self.current_wave}",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.GREEN, font_size=50, anchor_x="center", font_name="Impact")

        arcade.draw_text("Готовьтесь!",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=30, anchor_x="center", font_name="Impact")

        if self.current_wave > 1:
            y_offset = -120
            arcade.draw_text(f"Урон: {self.previous_wave_stats.get('total_damage', 0)}",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset,
                             arcade.color.YELLOW, font_size=20, anchor_x="center", font_name="Impact")
            y_offset -= 30
            arcade.draw_text(f"Убийства: {self.previous_wave_stats.get('kills', 0)}",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset,
                             arcade.color.YELLOW, font_size=20, anchor_x="center", font_name="Impact")
            y_offset -= 30
            arcade.draw_text(f"Время: {self.previous_wave_stats.get('time', 0):.1f} сек",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset,
                             arcade.color.YELLOW, font_size=20, anchor_x="center", font_name="Impact")

    def draw(self):
        if self.show_wave_screen:
            self.draw_wave_screen()

        elif self.show_upgrade_menu:
            self.upgrade_system.draw_upgrade_menu(50, SCREEN_HEIGHT - 100)
            self.upgrade_system.draw_active_upgrades(50, SCREEN_HEIGHT - 300)

            if self.show_upgrade_hint:
                arcade.draw_text("УЛУЧШЕНИЕ КУПЛЕНО!",
                                 SCREEN_WIDTH // 2, 200,
                                 arcade.color.GREEN, 30, anchor_x="center", font_name="Impact")

            arcade.draw_text("[ПРОБЕЛ] - ПРОДОЛЖИТЬ",
                             SCREEN_WIDTH // 2, 50,
                             arcade.color.LIGHT_GRAY, 16, anchor_x="center", font_name="Impact")

        elif self.wave_active:
            for zombie in self.zombies:
                zombie.draw()
            arcade.draw_text(f"Волна: {self.current_wave}",
                             10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18, font_name="Impact")
            arcade.draw_text(f"Зомби: {self.zombies_spawned - self.zombies_killed}/{self.zombies_spawned}",
                             10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 16, font_name="Impact")
