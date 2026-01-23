"""
Класс зомби, с их спавном с помощью AI и их характеристиками
"""

import arcade
import math
import random
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Zombie:
    class Stats:
        def __init__(self, health, speed, damage, points):
            self.max_health = health
            self.health = self.max_health
            self.speed = speed
            self.damage = damage
            self.points = points

    class AI:
        def __init__(self, zombie, player):
            self.zombie = zombie
            self.player = player

        def update(self, delta_time):
            dx = self.player.center_x - self.zombie.center_x
            dy = self.player.center_y - self.zombie.center_y
            distance = math.hypot(dx, dy)
            if distance > 0:
                dx /= distance
                dy /= distance
                self.zombie.center_x += dx * self.zombie.stats.speed * delta_time
                self.zombie.center_y += dy * self.zombie.stats.speed * delta_time

    def __init__(self, x, y, zombie_type="basic", wave=1):
        self.center_x = x
        self.center_y = y
        self.type = zombie_type

        self.frames = []

        frame_counts = {
            "basic": 16,
            "fast": 13,
            "fat": 8,
            "toxic": 8
        }

        frame_count = frame_counts.get(zombie_type, 4)

        for i in range(frame_count):
            if zombie_type == "basic":
                file_name = f"basic_zombie_{i}.png"
                folder = "basic"
            elif zombie_type == "fast":
                file_name = f"fast_zombie_{i}.png"
                folder = "fast"
            elif zombie_type == "fat":
                file_name = f"fat_zombie_{i}.png"
                folder = "fat"
            elif zombie_type == "toxic":
                file_name = f"toxic_zombie_{i}.png"
                folder = "toxic"
            else:
                file_name = f"basic_zombie_{i}.png"
                folder = "basic"

            path = f"assets/images/zombies/{folder}/{file_name}"
            texture = arcade.load_texture(path)
            self.frames.append(texture)

        self.health_bar_width = 40

        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.1

        base_health = {"basic": 50, "fast": 30,
                       "fat": 150, "toxic": 40}[zombie_type]
        base_speed = {"basic": 50, "fast": 100,
                      "fat": 30, "toxic": 70}[zombie_type]
        damage = {"basic": 10, "fast": 12,
                  "fat": 20, "toxic": 8}[zombie_type]
        points = {"basic": 10, "fast": 20,
                  "fat": 30, "toxic": 25}[zombie_type]

        health = int(base_health * (1 + (wave - 1) * 0.2))
        self.stats = self.Stats(
            health=health, speed=base_speed, damage=damage, points=points)

        self.ai = self.AI(self, None)

        self.width = 60 * 0.5 if zombie_type == "basic" else 45 * \
            0.5 if zombie_type == "fast" else 85 * 0.5 if zombie_type == "fat" else 65 * 0.5
        self.height = 89 * 0.5 if zombie_type == "basic" else 75 * \
            0.5 if zombie_type == "fast" else 170 * \
            0.5 if zombie_type == "fat" else 120 * 0.5

    def update(self, delta_time):
        self.ai.update(delta_time)

        self.animation_time += delta_time
        if self.animation_time >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_time = 0

    def draw(self):
        if not self.frames:
            return

        dx = self.ai.player.center_x - self.center_x if self.ai and self.ai.player else 0
        scale_x = self.width if dx >= 0 else -self.width

        texture = self.frames[self.current_frame]
        arcade.draw_texture_rect(
            texture,
            arcade.XYWH(
                self.center_x,
                self.center_y,
                scale_x,
                self.height
            )
        )

        if self.stats.health > 0:
            health_percent = self.stats.health / self.stats.max_health
            current_width = self.health_bar_width * health_percent

            arcade.draw_rect_filled(
                arcade.XYWH(self.center_x, self.center_y +
                            self.height / 2 + 10, self.health_bar_width, 6),
                arcade.color.DARK_GRAY
            )

            health_color = arcade.color.RED
            if health_percent > 0.5:
                health_color = arcade.color.ORANGE
            if health_percent > 0.75:
                health_color = arcade.color.GREEN

            arcade.draw_rect_filled(
                arcade.XYWH(self.center_x, self.center_y +
                            self.height / 2 + 10, current_width, 6),
                health_color
            )

            arcade.draw_rect_outline(
                arcade.XYWH(self.center_x, self.center_y +
                            self.height / 2 + 10, self.health_bar_width, 6),
                arcade.color.BLACK, border_width=1
            )

    def take_damage(self, damage):
        self.stats.health -= damage
        return self.stats.health <= 0

    def on_death(self):
        return self.stats.points
