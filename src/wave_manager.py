"""
Класс смены волн
"""

import arcade
import random
from .constants import (SCREEN_HEIGHT, SCREEN_WIDTH)
from .zombie import Zombie

SPAWN_MARGIN = 100
COLOR_WAVE_SCREEN = arcade.color.BLACK


class WaveManager:
    def __init__(self, player):
        self.player = player
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
        self.types = ["normal", "fast", "tank", "toxic"]
        self.show_player = True
        self.wave_stats = {}
        self.player_points = 0
        self.improvements = []

    def start_next_wave(self):
        self.current_wave += 1
        self.wave_active = False
        self.wave_timer = 0
        self.zombies_to_spawn = 5 + self.current_wave * 2
        self.zombies_spawned = 0
        self.zombies_killed = 0
        self.show_player = False
        self.wave_stats = {
            "total_damage": 0,
            "kills": 0,
            "time": 0
        }

    def update(self, delta_time):
        if not self.wave_active:
            self.wave_timer += delta_time
            if self.wave_timer >= self.wave_start_delay:
                self.wave_active = True
                self.show_player = True
        else:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval and self.zombies_spawned < self.zombies_to_spawn:
                self.spawn_zombie()
                self.spawn_timer = 0

            for zombie in self.zombies[:]:
                zombie.update(delta_time)

            self.update_wave_stats(delta_time)

            if self.zombies_spawned >= self.zombies_to_spawn and self.zombies_killed >= self.zombies_spawned:
                self.start_next_wave()

    def spawn_zombie(self):
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
        self.player_points += points
        return points

    def draw_wave_screen(self):
        arcade.draw_rect_filled(arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                                COLOR_WAVE_SCREEN)
        arcade.draw_text(f"ВОЛНА {self.current_wave}",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.GREEN, font_size=50, anchor_x="center", font_name="Impact")
        arcade.draw_text("Готовьтесь!",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=30, anchor_x="center", font_name="Impact")

        y_offset = -120
        arcade.draw_text(f"Урон: {self.wave_stats.get('total_damage', 0)}",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset,
                         arcade.color.YELLOW, font_size=20, anchor_x="center")
        y_offset -= 30
        arcade.draw_text(f"Убийства: {self.wave_stats.get('kills', 0)}",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset,
                         arcade.color.YELLOW, font_size=20, anchor_x="center")
        y_offset -= 30
        arcade.draw_text(f"Время: {self.wave_stats.get('time', 0):.1f} сек",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset,
                         arcade.color.YELLOW, font_size=20, anchor_x="center")

    def update_wave_stats(self, delta_time):
        if self.wave_active:
            self.wave_stats['time'] += delta_time

    # Покупка улучшения
    def buy_improvement(self, improvement_id, level):
        IMPROVEMENTS = [
            {'type': 'health', 'levels': [(20, 100), (40, 200), (60, 300)]},
            {'type': 'speed', 'levels': [(10, 150), (20, 300), (30, 450)]},
            {'type': 'damage', 'levels': [(15, 200), (30, 400), (50, 600)]},
            {'type': 'weapon', 'description': 'улучшить оружие'},
            {'type': 'special', 'description': 'особые способности'}
        ]
        imp = IMPROVEMENTS[improvement_id]
        cost = imp['levels'][level][1]
        if self.player_points >= cost:
            self.player_points -= cost
            print(f"Покупка совершена успешно!")
        else:
            print("Недостаточно очков для покупки.")

    def draw(self):
        if not self.wave_active and self.wave_timer < self.wave_start_delay:
            self.draw_wave_screen()
        else:
            for zombie in self.zombies:
                zombie.draw()

        if self.wave_active:
            arcade.draw_text(f"Волна: {self.current_wave}",
                             10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18, font_name="Impact")
            arcade.draw_text(f"Зомби: {self.zombies_spawned - self.zombies_killed}/{self.zombies_spawned}",
                             10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 16, font_name="Impact")
