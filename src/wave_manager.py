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

    def start_next_wave(self):
        self.current_wave += 1
        self.wave_active = False
        self.wave_timer = 0
        self.zombies_to_spawn = 5 + self.current_wave * 2
        self.zombies_spawned = 0
        self.zombies_killed = 0

    def update(self, delta_time):
        if not self.wave_active:
            self.wave_timer += delta_time
            if self.wave_timer >= self.wave_start_delay:
                self.wave_active = True
        else:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval and self.zombies_spawned < self.zombies_to_spawn:
                self.spawn_zombie()
                self.spawn_timer = 0

            for zombie in self.zombies[:]:
                zombie.update(delta_time)

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
        """Привязка ИИ к игроку"""
        zombie.ai = Zombie.AI(zombie, self.player)
        self.zombies.append(zombie)
        self.zombies_spawned += 1

    def kill_zombie(self, zombie):
        if zombie in self.zombies:
            self.zombies.remove(zombie)
        points = zombie.on_death()
        self.zombies_killed += 1
        return points

    def draw_wave_screen(self):
        """Отрисовка экрана между волнами"""
        arcade.draw_rect_filled(arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                                COLOR_WAVE_SCREEN)
        arcade.draw_text(f"ВОЛНА {self.current_wave}",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.GREEN, font_size=50, anchor_x="center", font_name="Impact")
        arcade.draw_text("Готовьтесь!",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=30, anchor_x="center", font_name="Impact")

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
